# backend/schemas.py

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

class PaperBase(BaseModel):
    pmid: str = Field(..., description="PubMed ID")
    title: str
    authors: Optional[str] = None
    journal: Optional[str] = None
    pub_date: Optional[datetime] = None
    abstract: Optional[str] = None
    url: Optional[str] = None
    study_type: Optional[str] = None

class PaperCreate(PaperBase):
    pass

class PaperOut(PaperBase):
    id: int
    fetched_at: datetime

    class Config:
        orm_mode = True

class FeedbackCreate(BaseModel):
    pmid: str
    feedback_type: str  # "interesting", "not_relevant", "already_knew", "save"

class TomorrowTopicCreate(BaseModel):
    topic: str

class TodayPaperResponse(BaseModel):
    paper: PaperOut
    recommendation_reason: str
    summary_en: str
    related: List[PaperOut] = []
    suggestions: List[PaperOut] = []
