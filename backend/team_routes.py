from fastapi import APIRouter, HTTPException, Header
from typing import Optional
import uuid
from datetime import datetime, timezone

from models import TeamInvite, RoleUpdate


def create_team_router(db, get_current_user, log_activity_fn, serialize_doc, serialize_list, get_password_hash):
    router = APIRouter(prefix="/api")

    async def require_auth(authorization):
        user = await get_current_user(authorization)
        if not user:
            raise HTTPException(401, "Oturum gecersiz")
        return user

    async def require_admin(authorization):
        user = await require_auth(authorization)
        if user.get("role", "admin") != "admin":
            raise HTTPException(403, "Bu islem sadece admin icin")
        return user

    # ==================== TEAM ====================

    @router.get("/team")
    async def list_team(authorization: Optional[str] = Header(None)):
        await require_auth(authorization)
        users = await db.users.find({}, {"_id": 0, "password_hash": 0}).sort("created_at", 1).to_list(100)
        return serialize_list(users)

    @router.post("/team/invite")
    async def invite_member(data: TeamInvite, authorization: Optional[str] = Header(None)):
        admin = await require_admin(authorization)
        existing = await db.users.find_one({"email": data.email})
        if existing:
            raise HTTPException(400, "Bu e-posta zaten kayitli")
        now = datetime.now(timezone.utc).isoformat()
        temp_password = str(uuid.uuid4())[:8]
        user = {
            "id": str(uuid.uuid4()),
            "email": data.email,
            "name": data.name or data.email.split("@")[0],
            "password_hash": get_password_hash(temp_password),
            "role": data.role,
            "status": "invited",
            "invited_by": admin.get("id", ""),
            "created_at": now,
        }
        await db.users.insert_one(user)
        await log_activity_fn("team_invite", f"'{data.email}' takim uyesi davet edildi ({data.role})", user["id"], "user", admin.get("id", ""))
        return {
            "id": user["id"],
            "email": user["email"],
            "name": user["name"],
            "role": user["role"],
            "status": user["status"],
            "temp_password": temp_password,
        }

    @router.put("/team/{user_id}/role")
    async def update_role(user_id: str, data: RoleUpdate, authorization: Optional[str] = Header(None)):
        admin = await require_admin(authorization)
        if admin.get("id") == user_id:
            raise HTTPException(400, "Kendi rolunuzu degistiremezsiniz")
        result = await db.users.update_one({"id": user_id}, {"$set": {"role": data.role}})
        if result.matched_count == 0:
            raise HTTPException(404, "Kullanici bulunamadi")
        updated = await db.users.find_one({"id": user_id}, {"_id": 0, "password_hash": 0})
        await log_activity_fn("role_changed", f"'{updated.get('name', '')}' rolu '{data.role}' olarak degistirildi", user_id, "user", admin.get("id", ""))
        return serialize_doc(updated)

    @router.delete("/team/{user_id}")
    async def remove_member(user_id: str, authorization: Optional[str] = Header(None)):
        admin = await require_admin(authorization)
        if admin.get("id") == user_id:
            raise HTTPException(400, "Kendinizi silemezsiniz")
        user = await db.users.find_one({"id": user_id}, {"_id": 0})
        if not user:
            raise HTTPException(404, "Kullanici bulunamadi")
        await db.users.delete_one({"id": user_id})
        await log_activity_fn("team_removed", f"'{user.get('name', '')}' takimdan cikarildi", user_id, "user", admin.get("id", ""))
        return {"message": "Kullanici silindi"}

    @router.put("/team/{user_id}/status")
    async def update_user_status(user_id: str, data: dict, authorization: Optional[str] = Header(None)):
        admin = await require_admin(authorization)
        new_status = data.get("status", "active")
        result = await db.users.update_one({"id": user_id}, {"$set": {"status": new_status}})
        if result.matched_count == 0:
            raise HTTPException(404, "Kullanici bulunamadi")
        updated = await db.users.find_one({"id": user_id}, {"_id": 0, "password_hash": 0})
        return serialize_doc(updated)

    # ==================== ACTIVITY LOG (ENHANCED) ====================

    @router.get("/activity-log")
    async def get_activity_log(
        entity_type: Optional[str] = None,
        user_id: Optional[str] = None,
        limit: int = 50,
        authorization: Optional[str] = Header(None)
    ):
        await require_auth(authorization)
        query = {}
        if entity_type and entity_type != "all":
            query["entity_type"] = entity_type
        if user_id:
            query["user_id"] = user_id
        activities = await db.activity_log.find(query, {"_id": 0}).sort("created_at", -1).to_list(limit)
        return serialize_list(activities)

    # ==================== SEGMENTS ====================

    @router.get("/segments/tags")
    async def get_all_tags(authorization: Optional[str] = Header(None)):
        await require_auth(authorization)
        # Get all unique tags from leads and clients
        lead_tags = await db.leads.distinct("tags")
        client_tags = await db.clients.distinct("tags")
        all_tags = list(set(lead_tags + client_tags))
        all_tags.sort()
        return all_tags

    @router.get("/segments/categories")
    async def get_all_categories(authorization: Optional[str] = Header(None)):
        await require_auth(authorization)
        categories = await db.clients.distinct("category")
        return [c for c in categories if c]

    return router
