# app/dependencies.py
from fastapi import HTTPException, Header
from app.db.supabase import supabase

def get_current_user(authorization: str = Header(...)) -> str:
    """Verify Supabase JWT and return user ID."""
    try:
        token = authorization.replace("Bearer ", "")
        user = supabase.auth.get_user(token)
        return user.user.id
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")