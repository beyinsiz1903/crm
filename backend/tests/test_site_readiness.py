"""Offline release acceptance tests. Never connects to an actual hotel or DB."""
import asyncio
import copy
import io
import os
import sys
import zipfile
from collections import defaultdict
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import httpx
import pytest
from fastapi import FastAPI

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
os.environ.setdefault('JWT_SECRET', 'offline-test-key-never-use-in-production-123')
os.environ.setdefault('MONGO_URL', 'mongodb://127.0.0.1:1')
from export_service import generate_full_html, create_export_zip, create_multipage_export_zip, _extract_image_urls
from publication import build_pages, broken_links, validate_publication
from site_safety import safe_url, safe_widget, public_address
from form_validation import validate_fields, CONTACT_FIELDS
from templates_data import generate_all_templates


@pytest.mark.parametrize('template', generate_all_templates(), ids=lambda t: t['id'])
@pytest.mark.parametrize('mode', ['single', 'multi'])
def test_every_template_has_visible_content_and_valid_links(template, mode):
    project = {**template, 'export_mode': mode}
    pages = build_pages(project)
    assert not broken_links(pages)
    assert 'sitemap.xml' in pages and 'robots.txt' in pages
    for name, source in pages.items():
        if name.endswith('.html'):
            assert '.page-section{display:none}' not in source
            assert '<details class="mobile-menu">' in source
            assert "if(e.target.tagName==='FORM')e.preventDefault()" not in source


@pytest.mark.parametrize('value', ['javascript:alert(1)', 'data:text/html,x', '//evil.example/path', 'https://x.example/\'onload=alert(1)', 'https://name:secret@example.com/'])
def test_dangerous_urls_are_rejected(value):
    assert safe_url(value) == ''


@pytest.mark.parametrize('ip', ['127.0.0.1', '10.0.0.1', '169.254.169.254', '::1', '::ffff:127.0.0.1', '192.168.1.1'])
def test_private_asset_addresses_are_rejected(ip):
    assert not public_address(ip)


def test_html_escaping_and_widget_isolation():
    project = {'name': '<script>alert(1)</script>', 'theme': {'headerFont': 'x;}</style><script>alert(2)</script>'}, 'sections': [{'type': 'hero', 'props': {'title': '<img src=x onerror=alert(3)>', 'ctaLink': 'javascript:alert(4)', 'ctaText': 'Test'}}]}
    source = generate_full_html(project)
    assert '<script>alert' not in source and '<img src=x' not in source and 'href="javascript:' not in source
    assert safe_widget('<script>alert(1)</script>') == ''
    widget = safe_widget('<iframe src="https://booking.example.com" onload="alert(1)"></iframe>')
    assert 'onload' not in widget and 'sandbox=' in widget


def test_booking_is_a_real_link_not_a_fake_post():
    source = generate_full_html({'sections': [{'type': 'booking', 'props': {'bookingUrl': 'https://booking.example.com'}}]})
    assert 'href="https://booking.example.com"' in source
    assert 'onsubmit="return false' not in source


def test_extensionless_images_and_local_uploads_are_discovered():
    assert 'https://images.example.com/photo-1?w=100' in _extract_image_urls('<img src="https://images.example.com/photo-1?w=100">')
    assert '/api/uploads/test.png' in _extract_image_urls('<img src="/api/uploads/test.png">')


def test_missing_booking_configuration_blocks_publish(monkeypatch):
    monkeypatch.setenv('PUBLIC_BASE_URL', 'https://crm.example.com')
    project = {'sections': [{'type': 'hero'}, {'type': 'booking', 'props': {}}]}
    assert any('Rezervasyon' in issue for issue in validate_publication(project))
    monkeypatch.delenv('PUBLIC_BASE_URL')
    assert any('PUBLIC_BASE_URL' in issue for issue in validate_publication(project))


def test_required_fields_email_and_spam_checks():
    from fastapi import HTTPException
    for fields in [{}, {'name': 'Test', 'email': 'bad', 'message': 'Test', 'consent': 'on'}, {'name': 'Test', 'email': 'a@example.com', 'message': 'Test', 'consent': 'on', 'website': 'spam'}]:
        with pytest.raises(HTTPException):
            validate_fields(CONTACT_FIELDS, fields)
    assert validate_fields(CONTACT_FIELDS, {'name': 'Test', 'email': 'a@example.com', 'message': 'Test', 'consent': 'on'})['name'] == 'Test'


def matches(row, query):
    for key, value in query.items():
        item = row.get(key)
        if isinstance(value, dict):
            if '$ne' in value and item == value['$ne']:
                return False
            if '$gte' in value and (item is None or item < value['$gte']):
                return False
        elif item != value:
            return False
    return True


class Cursor:
    def __init__(self, rows, projection=None):
        self.rows = copy.deepcopy(rows)
        if projection:
            self.rows = [{k: v for k, v in row.items() if projection.get(k) != 0} for row in self.rows]
    def sort(self, *_args): return self
    def limit(self, count): self.rows = self.rows[:count]; return self
    async def to_list(self, *_args): return self.rows


class Collection:
    def __init__(self): self.rows = []
    def find(self, query, projection=None): return Cursor([r for r in self.rows if matches(r, query)], projection)
    async def find_one(self, query, *args, **kwargs): return next((copy.deepcopy(r) for r in self.rows if matches(r, query)), None)
    async def insert_one(self, row): self.rows.append(copy.deepcopy(row))
    async def count_documents(self, query): return sum(matches(r, query) for r in self.rows)
    async def update_one(self, query, update, upsert=False):
        row = next((r for r in self.rows if matches(r, query)), None)
        if row is None and upsert:
            row = copy.deepcopy(query); self.rows.append(row)
        if row is None: return SimpleNamespace(matched_count=0)
        row.update(copy.deepcopy(update.get('$set', {})))
        for k, v in update.get('$inc', {}).items(): row[k] = row.get(k, 0) + v
        return SimpleNamespace(matched_count=1)


class FakeDB:
    def __init__(self): self.collections = defaultdict(Collection)
    def __getattr__(self, key): return self.collections[key]


@pytest.fixture
def app_and_db(monkeypatch):
    import server
    from content_routes import create_content_router
    db = FakeDB()
    db.projects.rows.append({'id': 'p1', 'name': 'Synthetic Hotel', 'sections': [{'type': 'hero', 'props': {'title': 'Version One'}}], 'theme': {}, 'published': False, 'updated_at': 'v1', 'export_mode': 'multi'})
    async def identity(authorization):
        if authorization == 'Bearer admin': return {'id': 'u1', 'role': 'admin', 'status': 'active'}
        if authorization == 'Bearer viewer': return {'id': 'u2', 'role': 'viewer', 'status': 'active'}
    async def log(*args): pass
    monkeypatch.setattr(server, 'db', db)
    monkeypatch.setattr(server, 'get_current_user', identity)
    monkeypatch.setenv('PUBLIC_BASE_URL', 'https://crm.example.com')
    app = FastAPI()
    app.middleware('http')(server.protect_management_api)
    app.include_router(server.api_router)
    app.include_router(create_content_router(db, identity, log, server.serialize_doc, server.serialize_list))
    return app, db


def run_request(app, method, path, **kwargs):
    async def call():
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='https://crm.example.com') as client:
            return await client.request(method, path, **kwargs)
    return asyncio.run(call())


@pytest.mark.parametrize('method,path,payload', [('GET', '/api/projects', None), ('PUT', '/api/projects/p1', {'name': 'Intruder'}), ('POST', '/api/projects/p1/publish', {}), ('POST', '/api/projects/p1/export', {}), ('GET', '/api/projects/p1/preview', None)])
def test_anonymous_management_is_rejected(app_and_db, method, path, payload):
    app, _ = app_and_db
    assert run_request(app, method, path, json=payload).status_code == 401


def test_viewer_cannot_modify_site(app_and_db):
    app, _ = app_and_db
    assert run_request(app, 'PUT', '/api/projects/p1', json={'name': 'Forbidden'}, headers={'Authorization': 'Bearer viewer'}).status_code == 403


def test_release_is_frozen_and_rollback_does_not_change_draft(app_and_db):
    app, db = app_and_db
    auth = {'Authorization': 'Bearer admin'}
    first = run_request(app, 'POST', '/api/projects/p1/publish', headers=auth)
    assert first.status_code == 200, first.text
    first_id = first.json()['release_id']
    assert 'Version One' in run_request(app, 'GET', '/api/hosted/p1/index.html').text
    changed = run_request(app, 'PUT', '/api/projects/p1', headers=auth, json={'sections': [{'type': 'hero', 'props': {'title': 'Version Two'}}]})
    assert changed.status_code == 200
    assert 'Version Two' not in run_request(app, 'GET', '/api/hosted/p1/index.html').text
    second = run_request(app, 'POST', '/api/projects/p1/publish', headers=auth)
    assert second.status_code == 200
    assert 'Version Two' in run_request(app, 'GET', '/api/hosted/p1/index.html').text
    assert run_request(app, 'POST', f'/api/projects/p1/releases/{first_id}/restore', headers=auth).status_code == 200
    assert 'Version One' in run_request(app, 'GET', '/api/hosted/p1/index.html').text
    assert db.projects.rows[0]['sections'][0]['props']['title'] == 'Version Two'
    assert run_request(app, 'PUT', '/api/projects/p1', headers=auth, json={'status': 'published'}).status_code == 422


def test_contact_submission_is_recorded_and_visible_in_forms(app_and_db):
    app, db = app_and_db
    auth = {'Authorization': 'Bearer admin'}
    assert run_request(app, 'POST', '/api/sites/p1/contact', json={}).status_code == 404
    assert run_request(app, 'POST', '/api/projects/p1/publish', headers=auth).status_code == 200
    assert run_request(app, 'POST', '/api/sites/p1/contact', json={}).status_code == 422
    result = run_request(app, 'POST', '/api/sites/p1/contact', json={'fields': {'name': 'Synthetic Test', 'email': 'test@example.com', 'message': 'Test', 'consent': 'on'}})
    assert result.status_code == 200 and result.json()['id']
    assert db.form_submissions.rows[0]['project_id'] == 'p1'
    assert db.forms.rows[0]['system_contact'] is True
    for _ in range(29):
        assert run_request(app, 'POST', '/api/sites/p1/contact', json={'fields': {'name': 'Synthetic Test', 'email': 'test@example.com', 'message': 'Test', 'consent': 'on'}}).status_code == 200
    assert run_request(app, 'POST', '/api/sites/p1/contact', json={'fields': {'name': 'Synthetic Test', 'email': 'test@example.com', 'message': 'Test', 'consent': 'on'}}).status_code == 429


def test_domain_verification_never_claims_fake_ssl(app_and_db):
    app, db = app_and_db
    db.domains.rows.append({'id': 'd1', 'domain': 'unconfigured.example.com'})
    result = run_request(app, 'POST', '/api/domains/d1/verify', headers={'Authorization': 'Bearer admin'})
    assert result.status_code == 409
    assert db.domains.rows[0]['ssl_status'] == 'not_configured'


def test_assets_are_pinned_to_public_addresses_without_private_network_calls():
    from asset_transport import PublicNetworkBackend
    with pytest.raises(ValueError):
        asyncio.run(PublicNetworkBackend().connect_tcp('127.0.0.1', 80))


@pytest.mark.parametrize('kind,value', [('number', 'NaN'), ('number', 'not a number'), ('date', '2026-02-30'), ('select', 'not offered')])
def test_form_rejects_invalid_typed_values(kind, value):
    from fastapi import HTTPException
    with pytest.raises(HTTPException):
        validate_fields([{'name': 'value', 'type': kind, 'options': 'One,Two'}], {'value': value})


def test_form_uses_published_schema_instead_of_draft(app_and_db):
    app, db = app_and_db
    db.forms.rows.append({'id': 'f1', 'project_id': 'p1', 'name': 'Fixture', 'status': 'active', 'fields': [{'name': 'original', 'label': 'Original', 'type': 'text', 'required': True}]})
    assert run_request(app, 'POST', '/api/projects/p1/publish', headers={'Authorization': 'Bearer admin'}).status_code == 200
    db.forms.rows[0]['fields'] = [{'name': 'unpublished', 'type': 'text', 'required': True}]
    result = run_request(app, 'POST', '/api/forms/f1/submit', json={'fields': {'original': 'Visitor saw this'}})
    assert result.status_code == 200, result.text
    assert db.form_submissions.rows[0]['data'] == {'original': 'Visitor saw this'}


def test_optional_unchecked_checkbox_is_valid():
    assert validate_fields([{'name': 'optional', 'type': 'checkbox'}], {'optional': False}) == {'optional': False}


def test_analytics_requires_privacy_and_can_be_revoked(monkeypatch):
    monkeypatch.setenv('PUBLIC_BASE_URL', 'https://crm.example.com')
    project = {'analytics': {'ga_id': 'G-TEST123'}, 'sections': [{'type': 'hero'}]}
    assert any('gizlilik' in issue for issue in validate_publication(project))
    source = generate_full_html(project)
    assert "window['ga-disable-G-TEST123']=true" in source
    assert "analytics_storage:'denied'" in source


@pytest.mark.parametrize('mode', ['single', 'multi'])
@pytest.mark.parametrize('bundle', [False, True])
def test_uploaded_images_are_copied_into_every_export(monkeypatch, tmp_path, mode, bundle):
    import export_service
    from PIL import Image
    image_path = tmp_path / 'fixture.png'
    Image.new('RGB', (2, 2), 'blue').save(image_path)
    monkeypatch.setattr(export_service, 'UPLOADS_DIR', tmp_path)
    project = {'name': 'Fixture', 'sections': [{'type': 'hero', 'props': {'title': 'Fixture', 'backgroundImage': '/api/uploads/fixture.png'}}]}
    if bundle:
        builder = export_service.create_export_zip_with_assets if mode == 'single' else export_service.create_multipage_export_zip_with_assets
        data = asyncio.run(builder(project))
    else:
        builder = create_export_zip if mode == 'single' else create_multipage_export_zip
        data = builder(project)
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        names = archive.namelist()
        assert 'Fixture/assets/fixture.png' in names
        assert archive.read('Fixture/assets/fixture.png') == image_path.read_bytes()
        assert b'assets/fixture.png' in archive.read('Fixture/index.html')


def test_image_url_entities_are_deduplicated():
    assert _extract_image_urls('<img src="https://images.example.com/a.jpg?w=10&amp;h=10">') == ['https://images.example.com/a.jpg?w=10&h=10']


def test_duplicate_form_names_do_not_silently_overwrite_data():
    from form_validation import validate_schema
    from fastapi import HTTPException
    with pytest.raises(HTTPException):
        validate_schema([{'label': 'Email 1', 'type': 'email'}, {'label': 'Email 2', 'type': 'email'}])
