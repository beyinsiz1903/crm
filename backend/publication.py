"""Publish immutable, validated releases, never the editor's mutable draft."""
import copy
import io
import os
import re
import uuid
import zipfile
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import PurePosixPath
from urllib.parse import urlsplit

from export_service import create_export_zip, create_multipage_export_zip
from site_safety import safe_widget, safe_url


class LinkInventory(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.ids = set()
        self.links = []
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('id'):
            self.ids.add(attrs['id'])
        if tag == 'a':
            self.links.append(attrs.get('href', ''))


def public_base():
    base = os.getenv('PUBLIC_BASE_URL', '').rstrip('/')
    if not base.startswith('https://') or not urlsplit(base).hostname or urlsplit(base).path:
        return ''
    return base


def validate_publication(project):
    issues = []
    if not public_base():
        issues.append('PUBLIC_BASE_URL ayarini gercek HTTPS yayin adresinizle yapilandirin.')
    visible = [s for s in project.get('sections', []) if s.get('visible', True)]
    if not any(s.get('type') == 'hero' for s in visible):
        issues.append('Gorunur bir ana sayfa bolumu ekleyin.')
    if any(s.get('type') == 'contact' for s in visible) and not project.get('legal', {}).get('privacy', '').strip():
        issues.append('Iletisim formu icin otelin gizlilik/acik riza bilgilendirmesini Ayarlar alanina girin.')
    for section in visible:
        props = section.get('props', {})
        if section.get('type') == 'booking':
            url = props.get('bookingUrl', '')
            widget = props.get('widgetCode', '')
            if not (url.startswith('https://') and safe_url(url)) and not safe_widget(widget):
                issues.append('Rezervasyon icin gercek HTTPS rezervasyon adresi veya guvenli iframe ekleyin.')
        if section.get('type') in {'contact', 'footer'}:
            for value in (props.get('phone', ''), props.get('email', '')):
                if '000 00 00' in value or 'info@otel.com' in value:
                    issues.append('Ornek telefon/e-posta yerine otelin gercek iletisim bilgilerini girin.')
        for key, value in props.get('socialLinks', {}).items():
            if value and (not value.startswith('https://') or not safe_url(value)):
                issues.append(f'{key} sosyal baglantisini doldurun veya kaldirin.')
        if props.get('widgetCode') and not safe_widget(props['widgetCode']):
            issues.append('Script widget desteklenmiyor; saglayicinin HTTPS iframe adresini kullanin.')
    if project.get('analytics', {}).get('custom_head_code'):
        issues.append('Guvenlik nedeniyle ham takip/script kodunu kaldirin; desteklenen GA kimligini kullanin.')
    ga_id = project.get('analytics', {}).get('ga_id', '')
    if ga_id and not re.fullmatch(r'G-[A-Z0-9]+', ga_id):
        issues.append('Google Analytics kimligi G- ile baslayan gecerli bir kimlik olmali.')
    if ga_id and not project.get('legal', {}).get('privacy', '').strip():
        issues.append('Analiz cerezi kullanimi icin gizlilik bilgilendirmesini girin.')
    return list(dict.fromkeys(issues))


def build_pages(project):
    builder = create_multipage_export_zip if project.get('export_mode') == 'multi' else create_export_zip
    archive = zipfile.ZipFile(io.BytesIO(builder(project)))
    pages = {PurePosixPath(name).name: archive.read(name).decode() for name in archive.namelist() if name.endswith(('.html', '.xml', 'robots.txt'))}
    for name, source in pages.items():
        pages[name] = source.replace('assets/', public_base() + '/api/uploads/')
    return pages


def broken_links(pages):
    parsed = {name: LinkInventory(source) for name, source in pages.items() if name.endswith('.html')}
    errors = []
    for name, page in parsed.items():
        for link in page.links:
            url = urlsplit(link)
            if url.scheme or url.netloc or link.startswith('/'):
                continue
            target = url.path or name
            if not link or link == '#' or target not in parsed or (url.fragment and url.fragment not in parsed[target].ids):
                errors.append(f'{name}: {link or "bos baglanti"}')
    return errors


async def make_release(project, db):
    snapshot = copy.deepcopy(project)
    snapshot.pop('release', None)
    base = public_base()
    snapshot['site_base_url'] = f'{base}/api/hosted/{project["id"]}/'
    snapshot['public_contact_url'] = f'{base}/api/sites/{project["id"]}/contact'
    snapshot = await enrich_public_content(snapshot, db)
    from form_validation import validate_schema
    for form in snapshot.get('public_forms', []):
        validate_schema(form.get('fields', []))
    pages = build_pages(snapshot)
    errors = broken_links(pages)
    if errors:
        from fastapi import HTTPException
        raise HTTPException(422, {'message': 'Kirik sayfa baglantilari var', 'issues': errors})
    return {'id': str(uuid.uuid4()), 'created_at': datetime.now(timezone.utc).isoformat(), 'pages': pages, 'snapshot': snapshot}


async def enrich_public_content(project, db):
    snapshot = copy.deepcopy(project)
    base = public_base()
    snapshot['public_contact_url'] = f'{base}/api/sites/{project["id"]}/contact' if base else ''
    snapshot['public_blog_posts'] = await db.blog_posts.find({'project_id': project['id'], 'status': 'published'}, {'_id': 0}).to_list(200)
    snapshot['public_forms'] = await db.forms.find({'project_id': project['id'], 'status': 'active', 'system_contact': {'$ne': True}}, {'_id': 0}).to_list(100)
    for form in snapshot['public_forms']:
        form['submit_url'] = f'{base}/api/forms/{form["id"]}/submit'
    return snapshot
