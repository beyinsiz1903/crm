from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
import uuid


# ============ TEMPLATES ============
class TemplateCreate(BaseModel):
    name: str
    category: str = "custom"
    description: str = ""
    thumbnail: str = ""
    theme: Optional[Dict[str, Any]] = None
    sections: Optional[List[Dict[str, Any]]] = None
    clone_from: Optional[str] = None


# ============ PROJECTS ============
class ProjectCreate(BaseModel):
    name: str
    template_id: str
    client_id: Optional[str] = None
    language: str = "tr"


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    client_id: Optional[str] = None
    theme: Optional[Dict[str, Any]] = None
    sections: Optional[List[Dict[str, Any]]] = None
    status: Optional[str] = None
    domain_notes: Optional[str] = None
    hosting_notes: Optional[str] = None
    seo: Optional[Dict[str, Any]] = None
    language: Optional[str] = None
    export_mode: Optional[str] = None  # "single" or "multi"
    analytics: Optional[Dict[str, Any]] = None  # {ga_id, custom_head_code}
    published: Optional[bool] = None
    bundle_assets: Optional[bool] = None


# ============ CLIENTS ============
class ClientCreate(BaseModel):
    hotel_name: str
    contact_name: str = ""
    email: str = ""
    phone: str = ""
    address: str = ""
    city: str = ""
    notes: str = ""


class ClientUpdate(BaseModel):
    hotel_name: Optional[str] = None
    contact_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    notes: Optional[str] = None


# ============ AUTH ============
class LoginRequest(BaseModel):
    email: str
    password: str


class RegisterRequest(BaseModel):
    email: str
    password: str
    name: str = "Admin"
