from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.responses import Response
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
import copy
from pathlib import Path
from typing import List, Optional
import uuid
from datetime import datetime, timezone

from models import (
    TemplateCreate, ProjectCreate, ProjectUpdate,
    ClientCreate, ClientUpdate
)
from templates_data import generate_all_templates
from export_service import generate_full_html, create_export_zip

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'syroce_crm')]

app = FastAPI(title="Syroce CRM API")
api_router = APIRouter(prefix="/api")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


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


async def log_activity(activity_type: str, message: str, entity_id: str = "", entity_type: str = ""):
    activity = {
        "id": str(uuid.uuid4()),
        "type": activity_type,
        "message": message,
        "entity_id": entity_id,
        "entity_type": entity_type,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    await db.activity_log.insert_one(activity)


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
    # Deep copy sections to avoid modifying template
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
    zip_bytes = create_export_zip(project)
    filename = project.get("name", "hotel-website").lower().replace(" ", "-")
    await log_activity("project_exported", f"'{project['name']}' projesi disari aktarildi", project_id, "project")
    return Response(
        content=zip_bytes,
        media_type="application/zip",
        headers={"Content-Disposition": f"attachment; filename={filename}.zip"}
    )


@api_router.post("/preview")
async def preview_html(data: dict):
    html = generate_full_html(data)
    return Response(content=html, media_type="text/html")


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
    # Remove old non-custom templates and re-seed
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
        logger.info(f"{count} sablon mevcut, yukleme atlanıyor")


# ==================== APP CONFIG ====================

app.include_router(api_router)

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
