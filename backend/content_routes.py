from fastapi import APIRouter, HTTPException, Header
from typing import Optional
import uuid
from datetime import datetime, timezone
import re
import hashlib
import os
from fastapi import Request
from form_validation import validate_fields, validate_schema, CONTACT_FIELDS

from models import FormCreate, FormUpdate, BlogPostCreate, BlogPostUpdate, DomainCreate


def create_content_router(db, get_current_user, log_activity_fn, serialize_doc, serialize_list):
    router = APIRouter(prefix="/api")

    async def require_auth(authorization):
        user = await get_current_user(authorization)
        if not user:
            raise HTTPException(401, "Oturum gecersiz")
        return user

    async def require_role(authorization, roles):
        user = await require_auth(authorization)
        if user.get("role", "viewer") not in roles:
            raise HTTPException(403, "Bu islem icin yetkiniz yok")
        return user

    # ==================== FORMS ====================

    @router.get("/forms")
    async def list_forms(
        project_id: Optional[str] = None,
        authorization: Optional[str] = Header(None)
    ):
        await require_auth(authorization)
        query = {}
        if project_id:
            query["project_id"] = project_id
        forms = await db.forms.find(query, {"_id": 0}).sort("updated_at", -1).to_list(100)
        return serialize_list(forms)

    @router.get("/forms/{form_id}")
    async def get_form(form_id: str, authorization: Optional[str] = Header(None)):
        await require_auth(authorization)
        form = await db.forms.find_one({"id": form_id}, {"_id": 0})
        if not form:
            raise HTTPException(404, "Form bulunamadi")
        return serialize_doc(form)

    @router.post("/forms")
    async def create_form(data: FormCreate, authorization: Optional[str] = Header(None)):
        user = await require_role(authorization, ["admin", "editor"])
        validate_schema(data.fields)
        now = datetime.now(timezone.utc).isoformat()
        form = {
            "id": str(uuid.uuid4()),
            "project_id": data.project_id,
            "name": data.name,
            "fields": data.fields,
            "form_type": data.form_type,
            "auto_create_lead": data.auto_create_lead,
            "status": "active",
            "submissions_count": 0,
            "created_by": user.get("id", ""),
            "created_at": now,
            "updated_at": now,
        }
        await db.forms.insert_one(form)
        await log_activity_fn("form_created", f"'{data.name}' formu olusturuldu", form["id"], "form", user.get("id", ""))
        return serialize_doc(form)

    @router.put("/forms/{form_id}")
    async def update_form(form_id: str, data: FormUpdate, authorization: Optional[str] = Header(None)):
        user = await require_role(authorization, ["admin", "editor"])
        if data.fields is not None:
            validate_schema(data.fields)
        update_data = {k: v for k, v in data.model_dump().items() if v is not None}
        update_data["updated_at"] = datetime.now(timezone.utc).isoformat()
        result = await db.forms.update_one({"id": form_id}, {"$set": update_data})
        if result.matched_count == 0:
            raise HTTPException(404, "Form bulunamadi")
        updated = await db.forms.find_one({"id": form_id}, {"_id": 0})
        return serialize_doc(updated)

    @router.delete("/forms/{form_id}")
    async def delete_form(form_id: str, authorization: Optional[str] = Header(None)):
        user = await require_role(authorization, ["admin"])
        result = await db.forms.delete_one({"id": form_id})
        if result.deleted_count == 0:
            raise HTTPException(404, "Form bulunamadi")
        await db.form_submissions.delete_many({"form_id": form_id})
        return {"message": "Form silindi"}

    @router.get("/forms/{form_id}/submissions")
    async def list_form_submissions(form_id: str, authorization: Optional[str] = Header(None)):
        await require_auth(authorization)
        subs = await db.form_submissions.find({"form_id": form_id}, {"_id": 0}).sort("created_at", -1).to_list(500)
        return serialize_list(subs)

    @router.post("/forms/{form_id}/submit")
    async def submit_form(form_id: str, data: dict, request: Request):
        """Public endpoint - no auth needed for form submissions."""
        form = await db.forms.find_one({"id": form_id}, {"_id": 0})
        if not form:
            raise HTTPException(404, "Form bulunamadi")
        if form.get("status") != "active":
            raise HTTPException(400, "Bu form aktif degil")
        if form.get('project_id'):
            project = await db.projects.find_one({'id': form['project_id'], 'published': True})
            if not project or not project.get('release'):
                raise HTTPException(404, 'Form yayinda degil')
            published_form = next((f for f in project['release']['snapshot'].get('public_forms', []) if f['id'] == form_id), None)
            if not published_form:
                raise HTTPException(404, 'Form yayindaki surumde bulunamadi')
            # Validate the schema the visitor actually saw, not an unpublished edit.
            form = published_form
        now = datetime.now(timezone.utc).isoformat()
        fields_data = validate_fields(form.get('fields', []), data.get('fields', data))
        ip = request.client.host if request.client else 'unknown'
        fingerprint = hashlib.sha256((os.environ.get('JWT_SECRET', '') + ip).encode()).hexdigest()
        from datetime import timedelta
        since = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()
        if await db.form_submissions.count_documents({'form_id': form_id, 'fingerprint': fingerprint, 'created_at': {'$gte': since}}) >= 30:
            raise HTTPException(429, 'Cok fazla gonderim; daha sonra tekrar deneyin')
        submission = {
            "id": str(uuid.uuid4()),
            "form_id": form_id,
            "data": fields_data,
            "created_at": now,
            "project_id": form.get('project_id', ''),
            "fingerprint": fingerprint,
        }
        await db.form_submissions.insert_one(submission)
        await db.forms.update_one({"id": form_id}, {"$inc": {"submissions_count": 1}})

        # Auto-create lead from form submission if enabled
        if form.get("auto_create_lead", False):
            lead_name = fields_data.get("name", fields_data.get("ad", fields_data.get("isim", "")))
            lead_email = fields_data.get("email", fields_data.get("eposta", ""))
            lead_phone = fields_data.get("phone", fields_data.get("telefon", ""))
            lead_company = fields_data.get("company", fields_data.get("sirket", fields_data.get("otel", "")))
            if lead_name or lead_email:
                auto_score = 0
                if lead_email:
                    auto_score += 10
                if lead_phone:
                    auto_score += 10
                if lead_company:
                    auto_score += 10
                lead = {
                    "id": str(uuid.uuid4()),
                    "name": lead_name or lead_email,
                    "email": lead_email,
                    "phone": lead_phone,
                    "company": lead_company,
                    "source": "website",
                    "score": auto_score,
                    "stage": "new",
                    "assigned_to": "",
                    "tags": ["form-submission"],
                    "notes": f"Form: {form.get('name', '')} | ID: {submission['id']}",
                    "created_by": "system",
                    "created_at": now,
                    "updated_at": now,
                }
                await db.leads.insert_one(lead)
                await log_activity_fn("lead_from_form", f"'{lead['name']}' form gonderiminden otomatik olusturuldu", lead["id"], "lead", "system")

        return {"message": "Form basariyla gonderildi", "id": submission["id"]}

    @router.post('/sites/{project_id}/contact')
    async def contact_site(project_id: str, data: dict, request: Request):
        project = await db.projects.find_one({'id': project_id, 'published': True}, {'_id': 0})
        if not project or not project.get('release'):
            raise HTTPException(404, 'Site yayinda degil')
        fields_data = validate_fields(CONTACT_FIELDS, data.get('fields', data))
        fingerprint = hashlib.sha256(((os.environ.get('JWT_SECRET') or '') + (request.client.host if request.client else 'unknown')).encode()).hexdigest()
        from datetime import timedelta
        since = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()
        form_id = f'site-contact-{project_id}'
        if await db.form_submissions.count_documents({'form_id': form_id, 'fingerprint': fingerprint, 'created_at': {'$gte': since}}) >= 30:
            raise HTTPException(429, 'Cok fazla gonderim; daha sonra tekrar deneyin')
        now = datetime.now(timezone.utc).isoformat()
        submission = {'id': str(uuid.uuid4()), 'form_id': form_id, 'project_id': project_id, 'data': fields_data, 'fingerprint': fingerprint, 'created_at': now}
        await db.form_submissions.insert_one(submission)
        await db.forms.update_one({'id': form_id}, {'$set': {'project_id': project_id, 'system_contact': True, 'name': f'{project["name"]} - Web iletisim', 'status': 'active', 'form_type': 'contact', 'fields': CONTACT_FIELDS, 'updated_at': now}, '$inc': {'submissions_count': 1}}, upsert=True)
        return {'id': submission['id'], 'message': 'Talebiniz kaydedildi'}

    # ==================== BLOG ====================

    def slugify(text):
        text = text.lower().strip()
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'[\s_]+', '-', text)
        text = re.sub(r'-+', '-', text)
        return text[:100]

    @router.get("/blog/posts")
    async def list_blog_posts(
        project_id: Optional[str] = None,
        status: Optional[str] = None,
        tag: Optional[str] = None,
        authorization: Optional[str] = Header(None)
    ):
        await require_auth(authorization)
        query = {}
        if project_id:
            query["project_id"] = project_id
        if status and status != "all":
            query["status"] = status
        if tag:
            query["tags"] = tag
        posts = await db.blog_posts.find(query, {"_id": 0}).sort("updated_at", -1).to_list(200)
        return serialize_list(posts)

    @router.get("/blog/posts/{post_id}")
    async def get_blog_post(post_id: str, authorization: Optional[str] = Header(None)):
        await require_auth(authorization)
        post = await db.blog_posts.find_one({"id": post_id}, {"_id": 0})
        if not post:
            raise HTTPException(404, "Yazi bulunamadi")
        return serialize_doc(post)

    @router.post("/blog/posts")
    async def create_blog_post(data: BlogPostCreate, authorization: Optional[str] = Header(None)):
        user = await require_role(authorization, ["admin", "editor"])
        now = datetime.now(timezone.utc).isoformat()
        slug = slugify(data.title)
        # Ensure unique slug
        existing = await db.blog_posts.find_one({"slug": slug, "project_id": data.project_id})
        if existing:
            slug = f"{slug}-{str(uuid.uuid4())[:8]}"
        post = {
            "id": str(uuid.uuid4()),
            "project_id": data.project_id,
            "title": data.title,
            "slug": slug,
            "content": data.content,
            "excerpt": data.excerpt,
            "cover_image": data.cover_image,
            "tags": data.tags,
            "status": data.status,
            "author": user.get("name", "Admin"),
            "author_id": user.get("id", ""),
            "created_at": now,
            "updated_at": now,
        }
        await db.blog_posts.insert_one(post)
        await log_activity_fn("blog_created", f"'{data.title}' blog yazisi olusturuldu", post["id"], "blog", user.get("id", ""))
        return serialize_doc(post)

    @router.put("/blog/posts/{post_id}")
    async def update_blog_post(post_id: str, data: BlogPostUpdate, authorization: Optional[str] = Header(None)):
        user = await require_role(authorization, ["admin", "editor"])
        update_data = {k: v for k, v in data.model_dump().items() if v is not None}
        update_data["updated_at"] = datetime.now(timezone.utc).isoformat()
        if "title" in update_data:
            update_data["slug"] = slugify(update_data["title"])
        result = await db.blog_posts.update_one({"id": post_id}, {"$set": update_data})
        if result.matched_count == 0:
            raise HTTPException(404, "Yazi bulunamadi")
        updated = await db.blog_posts.find_one({"id": post_id}, {"_id": 0})
        return serialize_doc(updated)

    @router.delete("/blog/posts/{post_id}")
    async def delete_blog_post(post_id: str, authorization: Optional[str] = Header(None)):
        user = await require_role(authorization, ["admin"])
        result = await db.blog_posts.delete_one({"id": post_id})
        if result.deleted_count == 0:
            raise HTTPException(404, "Yazi bulunamadi")
        return {"message": "Yazi silindi"}

    # ==================== DOMAINS (MOCK) ====================

    @router.get("/domains")
    async def list_domains(
        project_id: Optional[str] = None,
        authorization: Optional[str] = Header(None)
    ):
        await require_auth(authorization)
        query = {}
        if project_id:
            query["project_id"] = project_id
        domains = await db.domains.find(query, {"_id": 0}).sort("created_at", -1).to_list(50)
        return serialize_list(domains)

    @router.post("/domains")
    async def create_domain(data: DomainCreate, authorization: Optional[str] = Header(None)):
        user = await require_role(authorization, ["admin"])
        hostname = data.domain.strip().lower().rstrip('.')
        try:
            hostname = hostname.encode('idna').decode('ascii')
        except UnicodeError:
            raise HTTPException(422, 'Alan adi gecersiz')
        if not re.fullmatch(r'(?=.{1,253}$)(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,63}', hostname):
            raise HTTPException(422, 'Protokol, yol veya port icermeyen alan adi girin')
        now = datetime.now(timezone.utc).isoformat()
        domain = {
            "id": str(uuid.uuid4()),
            "project_id": data.project_id,
            "domain": hostname,
            "status": "configuration_required",
            "ssl_status": "not_configured",
            "dns_records": [],
            "created_by": user.get("id", ""),
            "created_at": now,
        }
        await db.domains.insert_one(domain)
        await log_activity_fn("domain_added", f"'{data.domain}' domaini eklendi", domain["id"], "domain", user.get("id", ""))
        return serialize_doc(domain)

    @router.delete("/domains/{domain_id}")
    async def delete_domain(domain_id: str, authorization: Optional[str] = Header(None)):
        user = await require_role(authorization, ["admin"])
        result = await db.domains.delete_one({"id": domain_id})
        if result.deleted_count == 0:
            raise HTTPException(404, "Domain bulunamadi")
        return {"message": "Domain silindi"}

    @router.post("/domains/{domain_id}/verify")
    async def verify_domain(domain_id: str, authorization: Optional[str] = Header(None)):
        user = await require_role(authorization, ["admin"])
        domain = await db.domains.find_one({"id": domain_id}, {"_id": 0})
        if not domain:
            raise HTTPException(404, "Domain bulunamadi")
        # Domain attachment/certificate provisioning needs a real hosting adapter.
        # A database flag can never establish DNS ownership or install TLS.
        await db.domains.update_one({'id': domain_id}, {'$set': {'status': 'configuration_required', 'ssl_status': 'not_configured'}})
        raise HTTPException(409, 'Otomatik domain/SSL saglayicisi yapilandirilmadi. Siteyi once paylasilan yayin adresinde yayinlayin; ozel domain icin hosting ve DNS kurulumu gerekli.')

    return router
