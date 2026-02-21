# app/models/schemas.py
from pydantic import BaseModel
from datetime import datetime


class AudioUploadResponse(BaseModel):
    message: str
    summary_id: str


class YouTubeResource(BaseModel):
    type: str
    title: str
    channel: str
    url: str
    thumbnail: str

class SummaryBase(BaseModel):
    title: str
    transcript: str
    summary: str
    topics: list[str]


class SummaryCreate(SummaryBase):
    user_id: str
    resources: dict[str, list[YouTubeResource]]


class SummaryResponse(SummaryBase):
    id: str
    user_id: str
    resources: dict[str, list[YouTubeResource]]
    created_at: datetime

    class Config:
        from_attributes = True



class SummaryListItem(BaseModel):
    id: str
    title: str
    created_at: datetime

    class Config:
        from_attributes = True