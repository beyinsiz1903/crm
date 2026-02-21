from fastapi import FastAPI, APIRouter, HTTPException, UploadFile, File, Depends, Header
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
import copy
from pathlib import Path
from typing import Optional
import uuid
from datetime import datetime, timezone, timedelta

from passlib.context import CryptContext
import jwt as pyjwt

from models import (
    TemplateCreate, ProjectCreate, ProjectUpdate,
    ClientCreate, ClientUpdate, LoginRequest, RegisterRequest
)
from templates_data import generate_all_templates
from export_service import (
    generate_full_html, create_export_zip, create_multipage_export_zip,
    create_export_zip_with_assets, create_multipage_export_zip_with_assets,
    TRANSLATIONS
)

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'syroce_crm')]

app = FastAPI(title="Syroce CRM API")
api_router = APIRouter(prefix="/api")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ==================== AUTH CONFIG ====================
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
JWT_SECRET = os.environ.get("JWT_SECRET", "syroce-crm-secret-key-2025-secure")
JWT_ALGORITHM = "HS256"

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_days=7):
    to_encode = data.copy()
    to_encode["exp"] = datetime.now(timezone.utc) + timedelta(days=expires_days)
    return pyjwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)

def decode_token(token: str):
    try:
        return pyjwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except Exception:
        return None

async def get_current_user(authorization: Optional[str] = Header(None)):
    if not authorization:
        return None
    try:
        scheme, token = authorization.split(" ", 1)
        if scheme.lower() != "bearer":
            return None
        payload = decode_token(token)
        if payload:
            user = await db.users.find_one({"id": payload.get("user_id")}, {"_id": 0})
            return user
    except Exception:
        pass
    return None

# ==================== UPLOADS ====================
UPLOAD_DIR = ROOT_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

# ==================== HELPERS ====================
def serialize_doc(doc):
    if doc is None:
        return None
    doc = dict(doc)
    doc.pop("_id", None)
    for key, value in doc.items():
        if isinstance(value, datetime):
            doc[key] = value.isoformat()
    return doc

def serialize_list(docs):
    return [serialize_doc(d) for d in docs]

async def log_activity(activity_type: str, message: str, entity_id: str = "", entity_type: str = "", user_id: str = ""):
    activity = {
        "id": str(uuid.uuid4()),
        "type": activity_type,
        "message": message,
        "entity_id": entity_id,
        "entity_type": entity_type,
        "user_id": user_id,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    await db.activity_log.insert_one(activity)

# ==================== AUTH ====================

@api_router.post("/auth/register")
async def register(data: RegisterRequest):
    existing = await db.users.find_one({"email": data.email})
    if existing:
        raise HTTPException(400, "Bu e-posta zaten kayitli")
    # First user is admin, others are editor by default
    user_count = await db.users.count_documents({})
    role = "admin" if user_count == 0 else "editor"
    user = {
        "id": str(uuid.uuid4()),
        "email": data.email,
        "name": data.name,
        "password_hash": get_password_hash(data.password),
        "role": role,
        "status": "active",
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    await db.users.insert_one(user)
    token = create_access_token({"user_id": user["id"], "email": user["email"], "role": role})
    return {"token": token, "user": {"id": user["id"], "email": user["email"], "name": user["name"], "role": role}}

@api_router.post("/auth/login")
async def login(data: LoginRequest):
    user = await db.users.find_one({"email": data.email}, {"_id": 0})
    if not user or not verify_password(data.password, user["password_hash"]):
        raise HTTPException(401, "Gecersiz e-posta veya sifre")
    role = user.get("role", "admin")
    token = create_access_token({"user_id": user["id"], "email": user["email"], "role": role})
    return {"token": token, "user": {"id": user["id"], "email": user["email"], "name": user.get("name", ""), "role": role}}

@api_router.get("/auth/me")
async def get_me(authorization: Optional[str] = Header(None)):
    user = await get_current_user(authorization)
    if not user:
        raise HTTPException(401, "Oturum gecersiz")
    return {"id": user["id"], "email": user["email"], "name": user.get("name", "")}

@api_router.get("/auth/check")
async def check_auth():
    count = await db.users.count_documents({})
    return {"has_users": count > 0}

# ==================== UPLOAD ====================

@api_router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    allowed = [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"]
    ext = Path(file.filename).suffix.lower() if file.filename else ""
    if ext not in allowed:
        raise HTTPException(400, f"Desteklenmeyen dosya formati. Izin verilen: {', '.join(allowed)}")
    content = await file.read()
    if len(content) > 5 * 1024 * 1024:
        raise HTTPException(400, "Dosya boyutu 5MB'yi asamaz")
    filename = f"{uuid.uuid4()}{ext}"
    filepath = UPLOAD_DIR / filename
    with open(filepath, "wb") as f:
        f.write(content)
    return {"url": f"/api/uploads/{filename}", "filename": filename}

# ==================== TEMPLATES ====================

@api_router.get("/templates")
async def list_templates(category: Optional[str] = None):
    query = {}
    if category and category != "all":
        query["category"] = category
    templates = await db.templates.find(query, {"_id": 0}).sort("name", 1).to_list(100)
    return serialize_list(templates)

@api_router.get("/templates/{template_id}")
async def get_template(template_id: str):
    template = await db.templates.find_one({"id": template_id}, {"_id": 0})
    if not template:
        raise HTTPException(status_code=404, detail="Template bulunamadi")
    return serialize_doc(template)

@api_router.post("/templates")
async def create_template(data: TemplateCreate):
    now = datetime.now(timezone.utc).isoformat()
    if data.clone_from:
        source = await db.templates.find_one({"id": data.clone_from}, {"_id": 0})
        if not source:
            raise HTTPException(status_code=404, detail="Kaynak template bulunamadi")
        template = dict(source)
        template["id"] = str(uuid.uuid4())
        template["name"] = data.name
        template["category"] = data.category or template.get("category", "custom")
        template["description"] = data.description or template.get("description", "")
        template["is_custom"] = True
        template["created_at"] = now
        template["updated_at"] = now
        if data.theme:
            template["theme"] = data.theme
        if data.sections:
            template["sections"] = data.sections
    else:
        template = {
            "id": str(uuid.uuid4()),
            "name": data.name,
            "category": data.category,
            "description": data.description,
            "thumbnail": data.thumbnail or "",
            "theme": data.theme or {},
            "sections": data.sections or [],
            "is_custom": True,
            "created_at": now,
            "updated_at": now,
        }
    template.pop("_id", None)
    await db.templates.insert_one(template)
    await log_activity("template_created", f"'{template['name']}' sablonu olusturuldu", template["id"], "template")
    return serialize_doc(template)

@api_router.post("/templates/clone-from-project/{project_id}")
async def clone_template_from_project(project_id: str, name: str = "Yeni Sablon", category: str = "custom"):
    project = await db.projects.find_one({"id": project_id}, {"_id": 0})
    if not project:
        raise HTTPException(404, "Proje bulunamadi")
    now = datetime.now(timezone.utc).isoformat()
    template = {
        "id": str(uuid.uuid4()),
        "name": name,
        "category": category,
        "description": f"'{project.get('name', '')}' projesinden olusturuldu",
        "thumbnail": "",
        "theme": copy.deepcopy(project.get("theme", {})),
        "sections": copy.deepcopy(project.get("sections", [])),
        "is_custom": True,
        "created_at": now,
        "updated_at": now,
    }
    # Get thumbnail from hero section
    for s in template["sections"]:
        if s.get("type") == "hero" and s.get("props", {}).get("backgroundImage"):
            template["thumbnail"] = s["props"]["backgroundImage"]
            break
    await db.templates.insert_one(template)
    await log_activity("template_created", f"'{name}' sablonu projeden olusturuldu", template["id"], "template")
    return serialize_doc(template)

@api_router.put("/templates/{template_id}")
async def update_template(template_id: str, data: dict):
    data["updated_at"] = datetime.now(timezone.utc).isoformat()
    data.pop("id", None)
    data.pop("_id", None)
    result = await db.templates.update_one({"id": template_id}, {"$set": data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Template bulunamadi")
    updated = await db.templates.find_one({"id": template_id}, {"_id": 0})
    return serialize_doc(updated)

@api_router.delete("/templates/{template_id}")
async def delete_template(template_id: str):
    result = await db.templates.delete_one({"id": template_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Template bulunamadi")
    return {"message": "Template silindi"}

# ==================== PROJECTS ====================

@api_router.get("/projects")
async def list_projects(status: Optional[str] = None):
    query = {}
    if status and status != "all":
        query["status"] = status
    projects = await db.projects.find(query, {"_id": 0}).sort("updated_at", -1).to_list(100)
    return serialize_list(projects)

@api_router.get("/projects/{project_id}")
async def get_project(project_id: str):
    project = await db.projects.find_one({"id": project_id}, {"_id": 0})
    if not project:
        raise HTTPException(status_code=404, detail="Proje bulunamadi")
    return serialize_doc(project)

@api_router.post("/projects")
async def create_project(data: ProjectCreate):
    template = await db.templates.find_one({"id": data.template_id}, {"_id": 0})
    if not template:
        raise HTTPException(status_code=404, detail="Template bulunamadi")
    now = datetime.now(timezone.utc).isoformat()
    sections = copy.deepcopy(template.get("sections", []))
    project = {
        "id": str(uuid.uuid4()),
        "name": data.name,
        "template_id": data.template_id,
        "client_id": data.client_id or "",
        "theme": copy.deepcopy(template.get("theme", {})),
        "sections": sections,
        "status": "draft",
        "domain_notes": "",
        "hosting_notes": "",
        "seo": {"title": "", "description": "", "keywords": "", "og_image": ""},
        "language": data.language or "tr",
        "export_mode": "single",
        "analytics": {"ga_id": "", "custom_head_code": ""},
        "published": False,
        "bundle_assets": False,
        "created_at": now,
        "updated_at": now,
    }
    await db.projects.insert_one(project)
    await log_activity("project_created", f"'{data.name}' projesi olusturuldu", project["id"], "project")
    return serialize_doc(project)

@api_router.put("/projects/{project_id}")
async def update_project(project_id: str, data: ProjectUpdate):
    update_data = {k: v for k, v in data.model_dump().items() if v is not None}
    update_data["updated_at"] = datetime.now(timezone.utc).isoformat()
    update_data.pop("id", None)
    result = await db.projects.update_one({"id": project_id}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Proje bulunamadi")
    updated = await db.projects.find_one({"id": project_id}, {"_id": 0})
    return serialize_doc(updated)

@api_router.delete("/projects/{project_id}")
async def delete_project(project_id: str):
    result = await db.projects.delete_one({"id": project_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Proje bulunamadi")
    await db.versions.delete_many({"project_id": project_id})
    return {"message": "Proje silindi"}

@api_router.get("/projects/{project_id}/preview")
async def preview_project(project_id: str):
    project = await db.projects.find_one({"id": project_id}, {"_id": 0})
    if not project:
        raise HTTPException(status_code=404, detail="Proje bulunamadi")
    html = generate_full_html(project)
    return Response(content=html, media_type="text/html")

@api_router.post("/projects/{project_id}/export")
async def export_project(project_id: str):
    project = await db.projects.find_one({"id": project_id}, {"_id": 0})
    if not project:
        raise HTTPException(status_code=404, detail="Proje bulunamadi")
    export_mode = project.get("export_mode", "single")
    bundle = project.get("bundle_assets", False)
    if bundle:
        if export_mode == "multi":
            zip_bytes = await create_multipage_export_zip_with_assets(project)
        else:
            zip_bytes = await create_export_zip_with_assets(project)
    else:
        if export_mode == "multi":
            zip_bytes = create_multipage_export_zip(project)
        else:
            zip_bytes = create_export_zip(project)
    filename = project.get("name", "hotel-website").lower().replace(" ", "-")
    await log_activity("project_exported", f"'{project['name']}' projesi disari aktarildi ({export_mode})", project_id, "project")
    return Response(
        content=zip_bytes,
        media_type="application/zip",
        headers={"Content-Disposition": f"attachment; filename={filename}.zip"}
    )

@api_router.post("/preview")
async def preview_html(data: dict):
    html = generate_full_html(data)
    return Response(content=html, media_type="text/html")

# ==================== PUBLISH / LIVE HOSTING ====================

@api_router.post("/projects/{project_id}/publish")
async def publish_project(project_id: str):
    project = await db.projects.find_one({"id": project_id}, {"_id": 0})
    if not project:
        raise HTTPException(404, "Proje bulunamadi")
    await db.projects.update_one(
        {"id": project_id},
        {"$set": {"published": True, "status": "published", "updated_at": datetime.now(timezone.utc).isoformat()}}
    )
    await log_activity("project_published", f"'{project['name']}' yayinlandi", project_id, "project")
    return {"published": True, "live_url": f"/api/hosted/{project_id}"}

@api_router.post("/projects/{project_id}/unpublish")
async def unpublish_project(project_id: str):
    project = await db.projects.find_one({"id": project_id}, {"_id": 0})
    if not project:
        raise HTTPException(404, "Proje bulunamadi")
    await db.projects.update_one(
        {"id": project_id},
        {"$set": {"published": False, "status": "draft", "updated_at": datetime.now(timezone.utc).isoformat()}}
    )
    await log_activity("project_unpublished", f"'{project['name']}' yayindan kaldirildi", project_id, "project")
    return {"published": False}

@api_router.get("/hosted/{project_id}")
async def hosted_project(project_id: str):
    """Serve published project as live website."""
    project = await db.projects.find_one({"id": project_id}, {"_id": 0})
    if not project:
        raise HTTPException(404, "Proje bulunamadi")
    if not project.get("published", False):
        raise HTTPException(403, "Bu proje henuz yayinlanmamis")
    html = generate_full_html(project)
    return Response(content=html, media_type="text/html")

# ==================== LANGUAGES ====================

@api_router.get("/languages")
async def get_available_languages():
    """Return all available languages for website generation."""
    lang_info = {
        "tr": {"name": "Turkce", "native": "Turkce", "flag": "TR"},
        "en": {"name": "English", "native": "English", "flag": "GB"},
        "de": {"name": "Almanca", "native": "Deutsch", "flag": "DE"},
        "fr": {"name": "Fransizca", "native": "Francais", "flag": "FR"},
        "es": {"name": "Ispanyolca", "native": "Espanol", "flag": "ES"},
        "it": {"name": "Italyanca", "native": "Italiano", "flag": "IT"},
        "ru": {"name": "Rusca", "native": "Russkiy", "flag": "RU"},
        "ar": {"name": "Arapca", "native": "العربية", "flag": "SA"},
        "ja": {"name": "Japonca", "native": "日本語", "flag": "JP"},
        "zh": {"name": "Cince", "native": "中文", "flag": "CN"},
    }
    return lang_info

# ==================== VERSIONING ====================

@api_router.get("/projects/{project_id}/versions")
async def list_versions(project_id: str):
    versions = await db.versions.find(
        {"project_id": project_id}, {"_id": 0, "theme": 0, "sections": 0, "seo": 0}
    ).sort("created_at", -1).to_list(50)
    return serialize_list(versions)

@api_router.post("/projects/{project_id}/versions")
async def create_version(project_id: str):
    project = await db.projects.find_one({"id": project_id}, {"_id": 0})
    if not project:
        raise HTTPException(404, "Proje bulunamadi")
    # Count existing versions
    count = await db.versions.count_documents({"project_id": project_id})
    version = {
        "id": str(uuid.uuid4()),
        "project_id": project_id,
        "version_number": count + 1,
        "label": f"v{count + 1}",
        "theme": copy.deepcopy(project.get("theme", {})),
        "sections": copy.deepcopy(project.get("sections", [])),
        "seo": copy.deepcopy(project.get("seo", {})),
        "language": project.get("language", "tr"),
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    await db.versions.insert_one(version)
    # Keep only last 20 versions
    if count >= 20:
        oldest = await db.versions.find({"project_id": project_id}).sort("created_at", 1).limit(1).to_list(1)
        if oldest:
            await db.versions.delete_one({"id": oldest[0]["id"]})
    return serialize_doc(version)

@api_router.post("/projects/{project_id}/restore/{version_id}")
async def restore_version(project_id: str, version_id: str):
    version = await db.versions.find_one({"id": version_id, "project_id": project_id}, {"_id": 0})
    if not version:
        raise HTTPException(404, "Versiyon bulunamadi")
    update_data = {
        "theme": version["theme"],
        "sections": version["sections"],
        "seo": version.get("seo", {}),
        "language": version.get("language", "tr"),
        "updated_at": datetime.now(timezone.utc).isoformat()
    }
    await db.projects.update_one({"id": project_id}, {"$set": update_data})
    updated = await db.projects.find_one({"id": project_id}, {"_id": 0})
    await log_activity("project_restored", f"Proje {version['label']} versiyonuna geri yuklendi", project_id, "project")
    return serialize_doc(updated)

# ==================== SECTION PRESETS (Block Library) ====================

@api_router.get("/section-presets")
async def list_section_presets(category: Optional[str] = None, section_type: Optional[str] = None):
    query = {}
    if category and category != "all":
        query["category"] = category
    if section_type:
        query["section_type"] = section_type
    presets = await db.section_presets.find(query, {"_id": 0}).sort("created_at", -1).to_list(100)
    return serialize_list(presets)

@api_router.post("/section-presets")
async def create_section_preset(data: dict):
    now = datetime.now(timezone.utc).isoformat()
    preset = {
        "id": str(uuid.uuid4()),
        "name": data.get("name", "Isimsiz Blok"),
        "category": data.get("category", "genel"),
        "section_type": data.get("section_type", ""),
        "props": data.get("props", {}),
        "created_at": now,
    }
    await db.section_presets.insert_one(preset)
    await log_activity("preset_created", f"'{preset['name']}' blok preseti olusturuldu", preset["id"], "preset")
    return serialize_doc(preset)

@api_router.delete("/section-presets/{preset_id}")
async def delete_section_preset(preset_id: str):
    result = await db.section_presets.delete_one({"id": preset_id})
    if result.deleted_count == 0:
        raise HTTPException(404, "Preset bulunamadi")
    return {"message": "Preset silindi"}

# ==================== CLIENTS ====================

@api_router.get("/clients")
async def list_clients(search: Optional[str] = None):
    query = {}
    if search:
        query["$or"] = [
            {"hotel_name": {"$regex": search, "$options": "i"}},
            {"contact_name": {"$regex": search, "$options": "i"}},
            {"city": {"$regex": search, "$options": "i"}},
        ]
    clients = await db.clients.find(query, {"_id": 0}).sort("hotel_name", 1).to_list(100)
    return serialize_list(clients)

@api_router.get("/clients/{client_id}")
async def get_client(client_id: str):
    c = await db.clients.find_one({"id": client_id}, {"_id": 0})
    if not c:
        raise HTTPException(status_code=404, detail="Musteri bulunamadi")
    return serialize_doc(c)

@api_router.post("/clients")
async def create_client(data: ClientCreate):
    now = datetime.now(timezone.utc).isoformat()
    client_doc = {
        "id": str(uuid.uuid4()),
        **data.model_dump(),
        "created_at": now,
        "updated_at": now,
    }
    await db.clients.insert_one(client_doc)
    await log_activity("client_added", f"'{data.hotel_name}' musterisi eklendi", client_doc["id"], "client")
    return serialize_doc(client_doc)

@api_router.put("/clients/{client_id}")
async def update_client(client_id: str, data: ClientUpdate):
    update_data = {k: v for k, v in data.model_dump().items() if v is not None}
    update_data["updated_at"] = datetime.now(timezone.utc).isoformat()
    result = await db.clients.update_one({"id": client_id}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Musteri bulunamadi")
    updated = await db.clients.find_one({"id": client_id}, {"_id": 0})
    return serialize_doc(updated)

@api_router.delete("/clients/{client_id}")
async def delete_client(client_id: str):
    result = await db.clients.delete_one({"id": client_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Musteri bulunamadi")
    return {"message": "Musteri silindi"}

# ==================== DASHBOARD ====================

@api_router.get("/dashboard/stats")
async def get_dashboard_stats():
    total_clients = await db.clients.count_documents({})
    total_projects = await db.projects.count_documents({})
    total_templates = await db.templates.count_documents({})
    draft_count = await db.projects.count_documents({"status": "draft"})
    published_count = await db.projects.count_documents({"status": "published"})
    delivered_count = await db.projects.count_documents({"status": "delivered"})
    return {
        "total_clients": total_clients,
        "total_projects": total_projects,
        "total_templates": total_templates,
        "status_distribution": {
            "draft": draft_count,
            "published": published_count,
            "delivered": delivered_count
        }
    }

@api_router.get("/dashboard/activity")
async def get_activity(limit: int = 20):
    activities = await db.activity_log.find({}, {"_id": 0}).sort("created_at", -1).to_list(limit)
    return serialize_list(activities)

# ==================== SEED ====================

@api_router.post("/seed")
async def seed_templates():
    count = await db.templates.count_documents({"is_custom": {"$ne": True}})
    if count >= 30:
        return {"message": "Sablonlar zaten mevcut", "count": count}
    await db.templates.delete_many({"is_custom": {"$ne": True}})
    templates = generate_all_templates()
    if templates:
        await db.templates.insert_many(templates)
    return {"message": f"{len(templates)} sablon yuklendi", "count": len(templates)}

@app.on_event("startup")
async def startup_event():
    count = await db.templates.count_documents({})
    if count < 30:
        logger.info("Sablonlar yukleniyor...")
        await db.templates.delete_many({"is_custom": {"$ne": True}})
        templates = generate_all_templates()
        if templates:
            await db.templates.insert_many(templates)
        logger.info(f"{len(templates)} sablon yuklendi")
    else:
        logger.info(f"{count} sablon mevcut")

# ==================== APP CONFIG ====================

app.include_router(api_router)

# Mount uploads AFTER router
app.mount("/api/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
