"""Opt-in integration test against disposable real MongoDB persistence."""
import asyncio
import os
import sys
import uuid
from pathlib import Path

import httpx
import pytest
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
os.environ.setdefault('JWT_SECRET', 'offline-test-key-never-use-in-production-123')
os.environ.setdefault('MONGO_URL', 'mongodb://127.0.0.1:1')


@pytest.mark.skipif(not os.getenv('TEST_MONGO_URL'), reason='Set TEST_MONGO_URL for disposable Mongo integration')
def test_real_auth_release_and_form_persistence(monkeypatch):
    import server
    from content_routes import create_content_router

    async def scenario():
        client = AsyncIOMotorClient(os.environ['TEST_MONGO_URL'], serverSelectionTimeoutMS=5000)
        # Never reuse a configured production database name or collection.
        name = 'crm_acceptance_' + uuid.uuid4().hex
        database = client[name]
        monkeypatch.setattr(server, 'db', database)
        monkeypatch.setenv('PUBLIC_BASE_URL', 'https://sites.example.invalid')
        app = FastAPI()
        app.middleware('http')(server.protect_management_api)
        app.include_router(server.api_router)
        app.include_router(create_content_router(database, server.get_current_user, server.log_activity, server.serialize_doc, server.serialize_list))
        try:
            await database.command('ping')
            async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url='https://sites.example.invalid') as http:
                registered = await http.post('/api/auth/register', json={'name': 'Synthetic Admin', 'email': 'test@example.invalid', 'password': 'LocalFixture2026!'})
                assert registered.status_code == 200, registered.text
                auth = {'Authorization': 'Bearer ' + registered.json()['token']}
                assert (await http.post('/api/auth/register', json={'name': 'Other', 'email': 'other@example.invalid', 'password': 'LocalFixture2026!'})).status_code == 403
                assert (await http.get('/api/projects')).status_code == 401
                assert (await http.post('/api/auth/login', json={'email': 'test@example.invalid', 'password': 'LocalFixture2026!'})).status_code == 200
                await database.templates.insert_one({'id': 'fixture', 'sections': [{'type': 'hero', 'props': {'title': 'Published One'}}], 'theme': {}})
                created = await http.post('/api/projects', headers=auth, json={'name': 'Synthetic Hotel', 'template_id': 'fixture'})
                assert created.status_code == 200, created.text
                project_id = created.json()['id']
                published = await http.post(f'/api/projects/{project_id}/publish', headers=auth)
                assert published.status_code == 200, published.text
                release_id = published.json()['release_id']
                assert await database.project_releases.count_documents({'project_id': project_id}) == 1
                assert (await http.put(f'/api/projects/{project_id}', headers=auth, json={'sections': [{'type': 'hero', 'props': {'title': 'Unpublished Two'}}]})).status_code == 200
                hosted = await http.get(f'/api/hosted/{project_id}/index.html')
                assert 'Published One' in hosted.text and 'Unpublished Two' not in hosted.text
                submitted = await http.post(f'/api/sites/{project_id}/contact', json={'fields': {'name': 'Synthetic Visitor', 'email': 'visitor@example.invalid', 'message': 'Fixture only', 'consent': 'on'}})
                assert submitted.status_code == 200, submitted.text
                forms = await http.get('/api/forms', headers=auth)
                form_id = forms.json()[0]['id']
                submissions = await http.get(f'/api/forms/{form_id}/submissions', headers=auth)
                assert submissions.json()[0]['data']['message'] == 'Fixture only'
                assert (await http.post(f'/api/projects/{project_id}/releases/{release_id}/restore', headers=auth)).status_code == 200
                assert (await database.projects.find_one({'id': project_id}))['sections'][0]['props']['title'] == 'Unpublished Two'
        finally:
            # Only this test's newly generated database is removed.
            await client.drop_database(name)
            client.close()

    asyncio.run(scenario())
