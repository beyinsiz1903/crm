from fastapi import APIRouter, HTTPException, Header, Query
from fastapi.responses import StreamingResponse
from typing import Optional, List
import uuid
import io
import csv
from datetime import datetime, timezone

from models import LeadCreate, LeadUpdate, CommunicationCreate, CampaignCreate, CampaignUpdate


def create_crm_router(db, get_current_user, log_activity_fn, serialize_doc, serialize_list):
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

    # ==================== LEADS ====================

    @router.get("/leads")
    async def list_leads(
        stage: Optional[str] = None,
        source: Optional[str] = None,
        assigned_to: Optional[str] = None,
        search: Optional[str] = None,
        tag: Optional[str] = None,
        sort_by: str = "updated_at",
        sort_dir: int = -1,
        page: int = 1,
        limit: int = 50,
        authorization: Optional[str] = Header(None)
    ):
        await require_auth(authorization)
        query = {}
        if stage and stage != "all":
            query["stage"] = stage
        if source and source != "all":
            query["source"] = source
        if assigned_to:
            query["assigned_to"] = assigned_to
        if tag:
            query["tags"] = tag
        if search:
            query["$or"] = [
                {"name": {"$regex": search, "$options": "i"}},
                {"email": {"$regex": search, "$options": "i"}},
                {"company": {"$regex": search, "$options": "i"}},
            ]
        total = await db.leads.count_documents(query)
        skip = (max(1, page) - 1) * limit
        leads = await db.leads.find(query, {"_id": 0}).sort(sort_by, sort_dir).skip(skip).limit(limit).to_list(limit)
        return {
            "items": serialize_list(leads),
            "total": total,
            "page": page,
            "limit": limit,
            "pages": max(1, (total + limit - 1) // limit)
        }

    @router.get("/leads/{lead_id}")
    async def get_lead(lead_id: str, authorization: Optional[str] = Header(None)):
        await require_auth(authorization)
        lead = await db.leads.find_one({"id": lead_id}, {"_id": 0})
        if not lead:
            raise HTTPException(404, "Lead bulunamadi")
        return serialize_doc(lead)

    @router.post("/leads")
    async def create_lead(data: LeadCreate, authorization: Optional[str] = Header(None)):
        user = await require_auth(authorization)
        now = datetime.now(timezone.utc).isoformat()
        # Auto-score
        auto_score = data.score
        if data.email:
            auto_score += 10
        if data.phone:
            auto_score += 10
        if data.company:
            auto_score += 10
        if data.source == "referral":
            auto_score += 20
        auto_score = min(auto_score, 100)

        lead = {
            "id": str(uuid.uuid4()),
            "name": data.name,
            "email": data.email,
            "phone": data.phone,
            "company": data.company,
            "source": data.source,
            "score": auto_score,
            "stage": data.stage,
            "assigned_to": data.assigned_to or user.get("id", ""),
            "tags": data.tags,
            "notes": data.notes,
            "created_by": user.get("id", ""),
            "created_at": now,
            "updated_at": now,
        }
        await db.leads.insert_one(lead)
        await log_activity_fn("lead_created", f"'{data.name}' lead'i olusturuldu", lead["id"], "lead", user.get("id", ""))
        return serialize_doc(lead)

    @router.put("/leads/{lead_id}")
    async def update_lead(lead_id: str, data: LeadUpdate, authorization: Optional[str] = Header(None)):
        user = await require_auth(authorization)
        update_data = {k: v for k, v in data.model_dump().items() if v is not None}
        update_data["updated_at"] = datetime.now(timezone.utc).isoformat()
        result = await db.leads.update_one({"id": lead_id}, {"$set": update_data})
        if result.matched_count == 0:
            raise HTTPException(404, "Lead bulunamadi")
        updated = await db.leads.find_one({"id": lead_id}, {"_id": 0})
        await log_activity_fn("lead_updated", f"'{updated.get('name', '')}' lead'i guncellendi", lead_id, "lead", user.get("id", ""))
        return serialize_doc(updated)

    @router.delete("/leads/{lead_id}")
    async def delete_lead(lead_id: str, authorization: Optional[str] = Header(None)):
        user = await require_role(authorization, ["admin", "editor"])
        lead = await db.leads.find_one({"id": lead_id}, {"_id": 0})
        if not lead:
            raise HTTPException(404, "Lead bulunamadi")
        await db.leads.delete_one({"id": lead_id})
        await db.communications.delete_many({"entity_id": lead_id})
        await log_activity_fn("lead_deleted", f"'{lead.get('name', '')}' lead'i silindi", lead_id, "lead", user.get("id", ""))
        return {"message": "Lead silindi"}

    @router.put("/leads/{lead_id}/stage")
    async def update_lead_stage(lead_id: str, data: dict, authorization: Optional[str] = Header(None)):
        user = await require_auth(authorization)
        stage = data.get("stage", "")
        if not stage:
            raise HTTPException(400, "Stage belirtilmeli")
        now = datetime.now(timezone.utc).isoformat()
        result = await db.leads.update_one({"id": lead_id}, {"$set": {"stage": stage, "updated_at": now}})
        if result.matched_count == 0:
            raise HTTPException(404, "Lead bulunamadi")
        updated = await db.leads.find_one({"id": lead_id}, {"_id": 0})
        await log_activity_fn("lead_stage_changed", f"'{updated.get('name', '')}' asamasi '{stage}' olarak degistirildi", lead_id, "lead", user.get("id", ""))
        return serialize_doc(updated)

    @router.put("/leads/{lead_id}/score")
    async def update_lead_score(lead_id: str, data: dict, authorization: Optional[str] = Header(None)):
        user = await require_auth(authorization)
        score = data.get("score", 0)
        now = datetime.now(timezone.utc).isoformat()
        result = await db.leads.update_one({"id": lead_id}, {"$set": {"score": min(max(score, 0), 100), "updated_at": now}})
        if result.matched_count == 0:
            raise HTTPException(404, "Lead bulunamadi")
        updated = await db.leads.find_one({"id": lead_id}, {"_id": 0})
        return serialize_doc(updated)

    @router.put("/leads/{lead_id}/assign")
    async def assign_lead(lead_id: str, data: dict, authorization: Optional[str] = Header(None)):
        user = await require_role(authorization, ["admin", "editor"])
        assigned_to = data.get("assigned_to", "")
        now = datetime.now(timezone.utc).isoformat()
        result = await db.leads.update_one({"id": lead_id}, {"$set": {"assigned_to": assigned_to, "updated_at": now}})
        if result.matched_count == 0:
            raise HTTPException(404, "Lead bulunamadi")
        updated = await db.leads.find_one({"id": lead_id}, {"_id": 0})
        await log_activity_fn("lead_assigned", f"'{updated.get('name', '')}' atandi", lead_id, "lead", user.get("id", ""))
        return serialize_doc(updated)

    # ==================== PIPELINE ====================

    @router.get("/pipeline/stages")
    async def list_pipeline_stages(authorization: Optional[str] = Header(None)):
        await require_auth(authorization)
        stages = await db.pipeline_stages.find({}, {"_id": 0}).sort("order", 1).to_list(20)
        if not stages:
            # Seed defaults
            defaults = [
                {"id": str(uuid.uuid4()), "name": "Yeni", "key": "new", "order": 0, "color": "#3B82F6"},
                {"id": str(uuid.uuid4()), "name": "Iletisime Gecildi", "key": "contacted", "order": 1, "color": "#F59E0B"},
                {"id": str(uuid.uuid4()), "name": "Nitelikli", "key": "qualified", "order": 2, "color": "#F97316"},
                {"id": str(uuid.uuid4()), "name": "Teklif", "key": "proposal", "order": 3, "color": "#8B5CF6"},
                {"id": str(uuid.uuid4()), "name": "Muzakere", "key": "negotiation", "order": 4, "color": "#6366F1"},
                {"id": str(uuid.uuid4()), "name": "Kazanildi", "key": "won", "order": 5, "color": "#10B981"},
                {"id": str(uuid.uuid4()), "name": "Kaybedildi", "key": "lost", "order": 6, "color": "#EF4444"},
            ]
            await db.pipeline_stages.insert_many(defaults)
            stages = defaults
        return serialize_list(stages)

    @router.get("/pipeline/board")
    async def get_pipeline_board(authorization: Optional[str] = Header(None)):
        await require_auth(authorization)
        stages = await db.pipeline_stages.find({}, {"_id": 0}).sort("order", 1).to_list(20)
        if not stages:
            # trigger stage creation
            stages = (await list_pipeline_stages(authorization))
            if isinstance(stages, list):
                pass
            else:
                stages = []
        leads = await db.leads.find({}, {"_id": 0}).to_list(1000)
        board = {}
        for stage in stages:
            key = stage.get("key", stage.get("name", "").lower())
            board[key] = {
                "stage": serialize_doc(stage),
                "leads": [serialize_doc(l) for l in leads if l.get("stage") == key],
                "total_value": 0,
            }
        return board

    @router.post("/pipeline/stages")
    async def create_pipeline_stage(data: dict, authorization: Optional[str] = Header(None)):
        await require_role(authorization, ["admin"])
        count = await db.pipeline_stages.count_documents({})
        stage = {
            "id": str(uuid.uuid4()),
            "name": data.get("name", "Yeni Asama"),
            "key": data.get("key", data.get("name", "new").lower().replace(" ", "_")),
            "order": data.get("order", count),
            "color": data.get("color", "#6B7280"),
        }
        await db.pipeline_stages.insert_one(stage)
        return serialize_doc(stage)

    @router.put("/pipeline/stages/{stage_id}")
    async def update_pipeline_stage(stage_id: str, data: dict, authorization: Optional[str] = Header(None)):
        await require_role(authorization, ["admin"])
        data.pop("id", None)
        data.pop("_id", None)
        result = await db.pipeline_stages.update_one({"id": stage_id}, {"$set": data})
        if result.matched_count == 0:
            raise HTTPException(404, "Asama bulunamadi")
        updated = await db.pipeline_stages.find_one({"id": stage_id}, {"_id": 0})
        return serialize_doc(updated)

    @router.delete("/pipeline/stages/{stage_id}")
    async def delete_pipeline_stage(stage_id: str, authorization: Optional[str] = Header(None)):
        await require_role(authorization, ["admin"])
        result = await db.pipeline_stages.delete_one({"id": stage_id})
        if result.deleted_count == 0:
            raise HTTPException(404, "Asama bulunamadi")
        return {"message": "Asama silindi"}

    # ==================== COMMUNICATIONS ====================

    @router.get("/communications")
    async def list_communications(
        entity_type: Optional[str] = None,
        entity_id: Optional[str] = None,
        authorization: Optional[str] = Header(None)
    ):
        await require_auth(authorization)
        query = {}
        if entity_type:
            query["entity_type"] = entity_type
        if entity_id:
            query["entity_id"] = entity_id
        comms = await db.communications.find(query, {"_id": 0}).sort("created_at", -1).to_list(200)
        return serialize_list(comms)

    @router.post("/communications")
    async def create_communication(data: CommunicationCreate, authorization: Optional[str] = Header(None)):
        user = await require_auth(authorization)
        now = datetime.now(timezone.utc).isoformat()
        comm = {
            "id": str(uuid.uuid4()),
            "entity_type": data.entity_type,
            "entity_id": data.entity_id,
            "comm_type": data.comm_type,
            "subject": data.subject,
            "content": data.content,
            "direction": data.direction,
            "created_by": user.get("id", ""),
            "created_by_name": user.get("name", ""),
            "created_at": now,
        }
        await db.communications.insert_one(comm)
        # Update lead/client score if communication added
        if data.entity_type == "lead":
            lead = await db.leads.find_one({"id": data.entity_id})
            if lead:
                new_score = min(lead.get("score", 0) + 5, 100)
                await db.leads.update_one({"id": data.entity_id}, {"$set": {"score": new_score, "updated_at": now}})
        entity_name = ""
        if data.entity_type == "lead":
            e = await db.leads.find_one({"id": data.entity_id})
            entity_name = e.get("name", "") if e else ""
        elif data.entity_type == "client":
            e = await db.clients.find_one({"id": data.entity_id})
            entity_name = e.get("hotel_name", "") if e else ""
        await log_activity_fn("communication_added", f"'{entity_name}' icin {data.comm_type} kaydedildi", data.entity_id, data.entity_type, user.get("id", ""))
        return serialize_doc(comm)

    @router.delete("/communications/{comm_id}")
    async def delete_communication(comm_id: str, authorization: Optional[str] = Header(None)):
        await require_auth(authorization)
        result = await db.communications.delete_one({"id": comm_id})
        if result.deleted_count == 0:
            raise HTTPException(404, "Kayit bulunamadi")
        return {"message": "Kayit silindi"}

    # ==================== CAMPAIGNS (MOCK) ====================

    @router.get("/campaigns")
    async def list_campaigns(
        status: Optional[str] = None,
        authorization: Optional[str] = Header(None)
    ):
        await require_auth(authorization)
        query = {}
        if status and status != "all":
            query["status"] = status
        campaigns = await db.campaigns.find(query, {"_id": 0}).sort("updated_at", -1).to_list(100)
        return serialize_list(campaigns)

    @router.get("/campaigns/{campaign_id}")
    async def get_campaign(campaign_id: str, authorization: Optional[str] = Header(None)):
        await require_auth(authorization)
        c = await db.campaigns.find_one({"id": campaign_id}, {"_id": 0})
        if not c:
            raise HTTPException(404, "Kampanya bulunamadi")
        return serialize_doc(c)

    @router.post("/campaigns")
    async def create_campaign(data: CampaignCreate, authorization: Optional[str] = Header(None)):
        user = await require_role(authorization, ["admin", "editor"])
        now = datetime.now(timezone.utc).isoformat()
        campaign = {
            "id": str(uuid.uuid4()),
            "name": data.name,
            "subject": data.subject,
            "content": data.content,
            "campaign_type": data.campaign_type,
            "status": "draft",
            "recipient_filter": data.recipient_filter,
            "steps": data.steps,
            "stats": {"sent": 0, "opened": 0, "clicked": 0, "bounced": 0},
            "created_by": user.get("id", ""),
            "created_at": now,
            "updated_at": now,
        }
        await db.campaigns.insert_one(campaign)
        await log_activity_fn("campaign_created", f"'{data.name}' kampanyasi olusturuldu", campaign["id"], "campaign", user.get("id", ""))
        return serialize_doc(campaign)

    @router.put("/campaigns/{campaign_id}")
    async def update_campaign(campaign_id: str, data: CampaignUpdate, authorization: Optional[str] = Header(None)):
        user = await require_role(authorization, ["admin", "editor"])
        update_data = {k: v for k, v in data.model_dump().items() if v is not None}
        update_data["updated_at"] = datetime.now(timezone.utc).isoformat()
        result = await db.campaigns.update_one({"id": campaign_id}, {"$set": update_data})
        if result.matched_count == 0:
            raise HTTPException(404, "Kampanya bulunamadi")
        updated = await db.campaigns.find_one({"id": campaign_id}, {"_id": 0})
        return serialize_doc(updated)

    @router.delete("/campaigns/{campaign_id}")
    async def delete_campaign(campaign_id: str, authorization: Optional[str] = Header(None)):
        user = await require_role(authorization, ["admin"])
        result = await db.campaigns.delete_one({"id": campaign_id})
        if result.deleted_count == 0:
            raise HTTPException(404, "Kampanya bulunamadi")
        return {"message": "Kampanya silindi"}

    @router.post("/campaigns/{campaign_id}/activate")
    async def activate_campaign(campaign_id: str, authorization: Optional[str] = Header(None)):
        user = await require_role(authorization, ["admin", "editor"])
        c = await db.campaigns.find_one({"id": campaign_id}, {"_id": 0})
        if not c:
            raise HTTPException(404, "Kampanya bulunamadi")
        import random
        # MOCK: simulate sending
        lead_count = await db.leads.count_documents({})
        mock_sent = random.randint(max(1, lead_count // 2), max(1, lead_count))
        mock_stats = {
            "sent": mock_sent,
            "opened": random.randint(0, mock_sent),
            "clicked": random.randint(0, mock_sent // 2) if mock_sent > 1 else 0,
            "bounced": random.randint(0, max(1, mock_sent // 10)),
        }
        await db.campaigns.update_one(
            {"id": campaign_id},
            {"$set": {"status": "active", "stats": mock_stats, "updated_at": datetime.now(timezone.utc).isoformat()}}
        )
        await log_activity_fn("campaign_activated", f"'{c['name']}' kampanyasi aktif edildi (MOCK)", campaign_id, "campaign", user.get("id", ""))
        updated = await db.campaigns.find_one({"id": campaign_id}, {"_id": 0})
        return serialize_doc(updated)

    @router.post("/campaigns/{campaign_id}/pause")
    async def pause_campaign(campaign_id: str, authorization: Optional[str] = Header(None)):
        user = await require_role(authorization, ["admin", "editor"])
        result = await db.campaigns.update_one(
            {"id": campaign_id},
            {"$set": {"status": "paused", "updated_at": datetime.now(timezone.utc).isoformat()}}
        )
        if result.matched_count == 0:
            raise HTTPException(404, "Kampanya bulunamadi")
        updated = await db.campaigns.find_one({"id": campaign_id}, {"_id": 0})
        return serialize_doc(updated)

    # ==================== REPORTS ====================

    @router.get("/reports/overview")
    async def reports_overview(authorization: Optional[str] = Header(None)):
        await require_auth(authorization)
        total_leads = await db.leads.count_documents({})
        won_leads = await db.leads.count_documents({"stage": "won"})
        lost_leads = await db.leads.count_documents({"stage": "lost"})
        total_clients = await db.clients.count_documents({})
        total_projects = await db.projects.count_documents({})
        total_campaigns = await db.campaigns.count_documents({})
        active_campaigns = await db.campaigns.count_documents({"status": "active"})
        total_comms = await db.communications.count_documents({})

        conversion_rate = round((won_leads / total_leads * 100), 1) if total_leads > 0 else 0

        # Lead source distribution
        sources = ["website", "referral", "social", "direct", "ad", "event", "other"]
        source_dist = {}
        for s in sources:
            count = await db.leads.count_documents({"source": s})
            if count > 0:
                source_dist[s] = count

        # Stage distribution
        stage_keys = ["new", "contacted", "qualified", "proposal", "negotiation", "won", "lost"]
        stage_dist = {}
        for sk in stage_keys:
            count = await db.leads.count_documents({"stage": sk})
            stage_dist[sk] = count

        # Average lead score
        pipeline = [{"$group": {"_id": None, "avg_score": {"$avg": "$score"}}}]
        avg_result = await db.leads.aggregate(pipeline).to_list(1)
        avg_score = round(avg_result[0]["avg_score"], 1) if avg_result else 0

        # Recent activity count (last 7 days)
        from datetime import timedelta
        week_ago = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()
        recent_activities = await db.activity_log.count_documents({"created_at": {"$gte": week_ago}})

        return {
            "total_leads": total_leads,
            "won_leads": won_leads,
            "lost_leads": lost_leads,
            "conversion_rate": conversion_rate,
            "total_clients": total_clients,
            "total_projects": total_projects,
            "total_campaigns": total_campaigns,
            "active_campaigns": active_campaigns,
            "total_communications": total_comms,
            "avg_lead_score": avg_score,
            "recent_activities": recent_activities,
            "source_distribution": source_dist,
            "stage_distribution": stage_dist,
        }

    @router.get("/reports/pipeline")
    async def reports_pipeline(authorization: Optional[str] = Header(None)):
        await require_auth(authorization)
        stages = await db.pipeline_stages.find({}, {"_id": 0}).sort("order", 1).to_list(20)
        result = []
        for stage in stages:
            key = stage.get("key", "")
            count = await db.leads.count_documents({"stage": key})
            result.append({
                "name": stage.get("name", ""),
                "key": key,
                "color": stage.get("color", "#6B7280"),
                "count": count,
            })
        return result

    @router.get("/reports/leads")
    async def reports_leads(authorization: Optional[str] = Header(None)):
        await require_auth(authorization)
        # Monthly lead creation trend (last 6 months)
        from datetime import timedelta
        now = datetime.now(timezone.utc)
        monthly = []
        for i in range(5, -1, -1):
            month_start = (now.replace(day=1) - timedelta(days=30 * i)).replace(day=1)
            if i > 0:
                month_end = (now.replace(day=1) - timedelta(days=30 * (i - 1))).replace(day=1)
            else:
                month_end = now
            count = await db.leads.count_documents({
                "created_at": {"$gte": month_start.isoformat(), "$lt": month_end.isoformat()}
            })
            monthly.append({
                "month": month_start.strftime("%Y-%m"),
                "label": month_start.strftime("%b"),
                "count": count,
            })

        # Top sources
        sources = ["website", "referral", "social", "direct", "ad", "event", "other"]
        source_data = []
        for s in sources:
            count = await db.leads.count_documents({"source": s})
            if count > 0:
                source_data.append({"source": s, "count": count})

        # Score distribution
        score_ranges = [(0, 20), (21, 40), (41, 60), (61, 80), (81, 100)]
        score_dist = []
        for low, high in score_ranges:
            count = await db.leads.count_documents({"score": {"$gte": low, "$lte": high}})
            score_dist.append({"range": f"{low}-{high}", "count": count})

        return {"monthly_trend": monthly, "source_data": source_data, "score_distribution": score_dist}

    @router.get("/reports/activity")
    async def reports_activity(days: int = 30, authorization: Optional[str] = Header(None)):
        await require_auth(authorization)
        from datetime import timedelta
        since = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
        activities = await db.activity_log.find(
            {"created_at": {"$gte": since}}, {"_id": 0}
        ).sort("created_at", -1).to_list(500)

        # Group by type
        type_counts = {}
        for a in activities:
            t = a.get("type", "other")
            type_counts[t] = type_counts.get(t, 0) + 1

        # Daily activity count
        daily = {}
        for a in activities:
            day = a.get("created_at", "")[:10]
            daily[day] = daily.get(day, 0) + 1

        daily_list = [{"date": k, "count": v} for k, v in sorted(daily.items())]

        return {"total": len(activities), "by_type": type_counts, "daily": daily_list, "recent": serialize_list(activities[:50])}

    # ==================== LEAD CONVERSION ====================

    @router.post("/leads/{lead_id}/convert")
    async def convert_lead_to_client(lead_id: str, authorization: Optional[str] = Header(None)):
        """Convert a lead to a client. Creates a client from lead data and marks lead as won."""
        user = await require_auth(authorization)
        lead = await db.leads.find_one({"id": lead_id}, {"_id": 0})
        if not lead:
            raise HTTPException(404, "Lead bulunamadi")
        if lead.get("stage") == "won" and lead.get("converted_client_id"):
            raise HTTPException(400, "Bu lead zaten donusturulmus")
        now = datetime.now(timezone.utc).isoformat()
        client_doc = {
            "id": str(uuid.uuid4()),
            "hotel_name": lead.get("company") or lead.get("name", ""),
            "contact_name": lead.get("name", ""),
            "email": lead.get("email", ""),
            "phone": lead.get("phone", ""),
            "address": "",
            "city": "",
            "notes": lead.get("notes", ""),
            "tags": lead.get("tags", []),
            "category": "",
            "custom_fields": {"lead_source": lead.get("source", ""), "lead_score": lead.get("score", 0)},
            "created_at": now,
            "updated_at": now,
        }
        await db.clients.insert_one(client_doc)
        await db.leads.update_one(
            {"id": lead_id},
            {"$set": {"stage": "won", "converted_client_id": client_doc["id"], "updated_at": now}}
        )
        await log_activity_fn("lead_converted", f"'{lead.get('name', '')}' musteri olarak donusturuldu", lead_id, "lead", user.get("id", ""))
        return {"message": "Lead basariyla musteriye donusturuldu", "client_id": client_doc["id"], "client": serialize_doc(client_doc)}

    # ==================== CSV EXPORT ====================

    @router.get("/leads/export/csv")
    async def export_leads_csv(authorization: Optional[str] = Header(None)):
        user = await require_auth(authorization)
        leads = await db.leads.find({}, {"_id": 0}).sort("created_at", -1).to_list(5000)
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Ad", "Email", "Telefon", "Sirket", "Kaynak", "Asama", "Skor", "Etiketler", "Notlar", "Olusturma Tarihi"])
        for lead in leads:
            writer.writerow([
                lead.get("name", ""), lead.get("email", ""), lead.get("phone", ""),
                lead.get("company", ""), lead.get("source", ""), lead.get("stage", ""),
                lead.get("score", 0), ", ".join(lead.get("tags", [])),
                lead.get("notes", ""), lead.get("created_at", "")[:10]
            ])
        output.seek(0)
        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=leads_export.csv"}
        )

    @router.get("/clients/export/csv")
    async def export_clients_csv(authorization: Optional[str] = Header(None)):
        user = await require_auth(authorization)
        clients = await db.clients.find({}, {"_id": 0}).sort("hotel_name", 1).to_list(5000)
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Otel Adi", "Yetkili Kisi", "Email", "Telefon", "Adres", "Sehir", "Kategori", "Etiketler", "Notlar", "Olusturma Tarihi"])
        for c in clients:
            writer.writerow([
                c.get("hotel_name", ""), c.get("contact_name", ""), c.get("email", ""),
                c.get("phone", ""), c.get("address", ""), c.get("city", ""),
                c.get("category", ""), ", ".join(c.get("tags", [])),
                c.get("notes", ""), c.get("created_at", "")[:10]
            ])
        output.seek(0)
        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=clients_export.csv"}
        )

    # ==================== BULK OPERATIONS ====================

    @router.post("/leads/bulk/stage")
    async def bulk_update_stage(data: dict, authorization: Optional[str] = Header(None)):
        user = await require_role(authorization, ["admin", "editor"])
        lead_ids = data.get("lead_ids", [])
        stage = data.get("stage", "")
        if not lead_ids or not stage:
            raise HTTPException(400, "lead_ids ve stage gerekli")
        now = datetime.now(timezone.utc).isoformat()
        result = await db.leads.update_many(
            {"id": {"$in": lead_ids}},
            {"$set": {"stage": stage, "updated_at": now}}
        )
        await log_activity_fn("bulk_stage_update", f"{result.modified_count} lead asamasi '{stage}' olarak degistirildi", "", "lead", user.get("id", ""))
        return {"message": f"{result.modified_count} lead guncellendi"}

    @router.post("/leads/bulk/delete")
    async def bulk_delete_leads(data: dict, authorization: Optional[str] = Header(None)):
        user = await require_role(authorization, ["admin"])
        lead_ids = data.get("lead_ids", [])
        if not lead_ids:
            raise HTTPException(400, "lead_ids gerekli")
        result = await db.leads.delete_many({"id": {"$in": lead_ids}})
        await db.communications.delete_many({"entity_id": {"$in": lead_ids}})
        await log_activity_fn("bulk_delete", f"{result.deleted_count} lead silindi", "", "lead", user.get("id", ""))
        return {"message": f"{result.deleted_count} lead silindi"}

    return router
