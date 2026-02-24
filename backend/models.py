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
    tags: List[str] = []
    category: str = ""
    custom_fields: Dict[str, Any] = {}


class ClientUpdate(BaseModel):
    hotel_name: Optional[str] = None
    contact_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    notes: Optional[str] = None
    tags: Optional[List[str]] = None
    category: Optional[str] = None
    custom_fields: Optional[Dict[str, Any]] = None


# ============ AUTH ============
class LoginRequest(BaseModel):
    email: str
    password: str


class RegisterRequest(BaseModel):
    email: str
    password: str
    name: str = "Admin"


# ============ LEADS ============
class LeadCreate(BaseModel):
    name: str
    email: str = ""
    phone: str = ""
    company: str = ""
    source: str = "direct"
    score: int = 0
    stage: str = "new"
    assigned_to: str = ""
    tags: List[str] = []
    notes: str = ""


class LeadUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    source: Optional[str] = None
    score: Optional[int] = None
    stage: Optional[str] = None
    assigned_to: Optional[str] = None
    tags: Optional[List[str]] = None
    notes: Optional[str] = None


# ============ COMMUNICATIONS ============
class CommunicationCreate(BaseModel):
    entity_type: str  # "lead" or "client"
    entity_id: str
    comm_type: str  # "email", "phone", "meeting", "note"
    subject: str = ""
    content: str = ""
    direction: str = "outbound"


# ============ CAMPAIGNS (MOCK) ============
class CampaignCreate(BaseModel):
    name: str
    subject: str = ""
    content: str = ""
    campaign_type: str = "single"
    recipient_filter: Dict[str, Any] = {}
    steps: List[Dict[str, Any]] = []


class CampaignUpdate(BaseModel):
    name: Optional[str] = None
    subject: Optional[str] = None
    content: Optional[str] = None
    status: Optional[str] = None
    recipient_filter: Optional[Dict[str, Any]] = None
    steps: Optional[List[Dict[str, Any]]] = None


# ============ FORMS ============
class FormCreate(BaseModel):
    project_id: str = ""
    name: str
    fields: List[Dict[str, Any]] = []
    form_type: str = "contact"


class FormUpdate(BaseModel):
    name: Optional[str] = None
    fields: Optional[List[Dict[str, Any]]] = None
    form_type: Optional[str] = None
    status: Optional[str] = None


# ============ BLOG ============
class BlogPostCreate(BaseModel):
    project_id: str
    title: str
    content: str = ""
    excerpt: str = ""
    cover_image: str = ""
    tags: List[str] = []
    status: str = "draft"


class BlogPostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    excerpt: Optional[str] = None
    cover_image: Optional[str] = None
    tags: Optional[List[str]] = None
    status: Optional[str] = None


# ============ DOMAINS ============
class DomainCreate(BaseModel):
    project_id: str
    domain: str


# ============ TEAM ============
class TeamInvite(BaseModel):
    email: str
    name: str = ""
    role: str = "editor"


class RoleUpdate(BaseModel):
    role: str


# ============ PROFILE ============
class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None


class PasswordChange(BaseModel):
    current_password: str
    new_password: str


# ============ NOTIFICATIONS ============
class NotificationCreate(BaseModel):
    title: str
    message: str
    type: str = "info"  # info, success, warning, error
    link: str = ""
