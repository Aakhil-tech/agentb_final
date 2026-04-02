from fastapi import APIRouter, HTTPException
from database import supabase

router = APIRouter()

@router.get("/incidents")
async def get_incidents(api_key: str):
    if not api_key:
        raise HTTPException(status_code=400, detail="api_key required")
    if supabase is None:
        raise HTTPException(
            status_code=500,
            detail="Supabase is not configured. Set SUPABASE_URL and SUPABASE_KEY.",
        )

    result = supabase.table("logs")\
        .select("*")\
        .eq("api_key", api_key)\
        .eq("flagged", True)\
        .order("created_at", desc=True)\
        .execute()

    return result.data

@router.get("/incidents/{incident_id}")
async def get_incident_detail(incident_id: str, api_key: str):
    if supabase is None:
        raise HTTPException(
            status_code=500,
            detail="Supabase is not configured. Set SUPABASE_URL and SUPABASE_KEY.",
        )
    result = supabase.table("logs")\
        .select("*")\
        .eq("id", incident_id)\
        .eq("api_key", api_key)\
        .execute()

    if not result.data:
        raise HTTPException(status_code=404, detail="Incident not found")

    return result.data[0]