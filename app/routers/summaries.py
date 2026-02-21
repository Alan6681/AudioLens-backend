from fastapi import APIRouter, HTTPException, Depends
from app.models.schema import SummaryResponse, SummaryListItem
from app.db.queries import get_summary_by_id, get_summaries_by_user, delete_summary
from app.dependencies import get_current_user

router = APIRouter(prefix="/summaries", tags=["summaries"])


@router.get("/", response_model=list[SummaryListItem])
def get_all_summaries(user_id: str = Depends(get_current_user)):
    summaries = get_summaries_by_user(user_id)
    return summaries


@router.get("/{summary_id}", response_model=SummaryResponse)
def get_summary(summary_id: str, user_id: str = Depends(get_current_user)):
    summary = get_summary_by_id(summary_id)

    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")

    if summary["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    return summary


@router.delete("/{summary_id}")
def remove_summary(summary_id: str, user_id: str = Depends(get_current_user)):
    deleted = delete_summary(summary_id, user_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Summary not found or access denied")

    return {"message": "Summary deleted successfully"}