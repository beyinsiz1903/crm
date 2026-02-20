from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
import uuid


class ThemeConfig(BaseModel):
    primaryColor: str = "#C5A572"
    secondaryColor: str = "#1A1A2E"
    backgroundColor: str = "#FFFFFF"
    textColor: str = "#333333"
    accentColor: str = "#8B6914"
    headerFont: str = "'Playfair Display', serif"
    bodyFont: str = "'Lato', sans-serif"


class TemplateCreate(BaseModel):
    name: str
    category: str = "custom"
    description: str = ""
    thumbnail: str = ""
    theme: Optional[Dict[str, Any]] = None
    sections: Optional[List[Dict[str, Any]]] = None
    clone_from: Optional[str] = None


class ProjectCreate(BaseModel):
    name: str
    template_id: str
    client_id: Optional[str] = None


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    client_id: Optional[str] = None
    theme: Optional[Dict[str, Any]] = None
    sections: Optional[List[Dict[str, Any]]] = None
    status: Optional[str] = None
    domain_notes: Optional[str] = None
    hosting_notes: Optional[str] = None


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
