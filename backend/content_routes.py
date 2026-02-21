from fastapi import APIRouter, HTTPException, Header
from typing import Optional
import uuid
from datetime import datetime, timezone
import re

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
        if user.get("role", "admin") not in roles:
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
        now = datetime.now(timezone.utc).isoformat()
        form = {
            "id": str(uuid.uuid4()),
            "project_id": data.project_id,
            "name": data.name,
            "fields": data.fields,
            "form_type": data.form_type,
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
    async def submit_form(form_id: str, data: dict):
        """Public endpoint - no auth needed for form submissions."""
        form = await db.forms.find_one({"id": form_id}, {"_id": 0})
        if not form:
            raise HTTPException(404, "Form bulunamadi")
        if form.get("status") != "active":
            raise HTTPException(400, "Bu form aktif degil")
        now = datetime.now(timezone.utc).isoformat()
        submission = {
            "id": str(uuid.uuid4()),
            "form_id": form_id,
            "data": data.get("fields", data),
            "created_at": now,
        }
        await db.form_submissions.insert_one(submission)
        await db.forms.update_one({"id": form_id}, {"$inc": {"submissions_count": 1}})
        return {"message": "Form basariyla gonderildi", "id": submission["id"]}

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
        now = datetime.now(timezone.utc).isoformat()
        domain = {
            "id": str(uuid.uuid4()),
            "project_id": data.project_id,
            "domain": data.domain.strip().lower(),
            "status": "pending",
            "ssl_status": "pending",
            "dns_records": [
                {"type": "CNAME", "name": "www", "value": "hosting.syroce.com", "status": "pending"},
                {"type": "A", "name": "@", "value": "185.199.108.153", "status": "pending"},
            ],
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
        import random
        # MOCK verification
        verified = random.choice([True, True, True, False])  # 75% success
        new_status = "verified" if verified else "failed"
        ssl_status = "active" if verified else "pending"
        dns_records = domain.get("dns_records", [])
        for r in dns_records:
            r["status"] = "verified" if verified else "pending"

        await db.domains.update_one(
            {"id": domain_id},
            {"$set": {"status": new_status, "ssl_status": ssl_status, "dns_records": dns_records}}
        )
        updated = await db.domains.find_one({"id": domain_id}, {"_id": 0})
        if verified:
            await log_activity_fn("domain_verified", f"'{domain['domain']}' dogrulandi", domain_id, "domain", user.get("id", ""))
        return serialize_doc(updated)

    return router
