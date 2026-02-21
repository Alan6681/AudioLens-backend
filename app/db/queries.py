# app/db/queries.py
from datetime import datetime
from app.db.supabase import supabase


# ─── Summaries ─────────────────────────────────────────────

def save_summary(
    user_id: str,
    title: str,
    transcript: str,
    summary: str,
    topics: list[str],
    resources: dict,
) -> dict:
    """Save a completed pipeline result to Supabase."""
    data = {
        "user_id": user_id,
        "title": title,
        "transcript": transcript,
        "summary": summary,
        "topics": topics,
        "resources": resources,
        "created_at": datetime.utcnow().isoformat(),
    }

    response = supabase.table("summaries").insert(data).execute()

    if not response.data:
        raise Exception("Failed to save summary to database")

    return response.data[0]


def get_summary_by_id(summary_id: str) -> dict | None:
    """Fetch a single summary by its ID."""
    response = (
        supabase.table("summaries")
        .select("*")
        .eq("id", summary_id)
        .single()
        .execute()
    )

    return response.data


def get_summaries_by_user(user_id: str) -> list[dict]:
    """Fetch all summaries belonging to a user."""
    response = (
        supabase.table("summaries")
        .select("id, title, created_at")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .execute()
    )

    return response.data or []


def delete_summary(summary_id: str, user_id: str) -> bool:
    """Delete a summary — only if it belongs to the user."""
    response = (
        supabase.table("summaries")
        .delete()
        .eq("id", summary_id)
        .eq("user_id", user_id)
        .execute()
    )

    return bool(response.data)