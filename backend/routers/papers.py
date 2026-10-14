# backend/routers/papers.py

"""API routes for the MVP.
- GET /today : retrieve today's paper (random from stub data for now)
- POST /feedback : record user feedback
- POST /tomorrow : store tomorrow's topic
- GET /related : placeholder for related papers (returns empty list)
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas, database, pubmed_client

router = APIRouter()

# Dependency
get_db = database.get_db

# Helper to get or create a single dummy user (MVP assumes one user)
def get_user(db: Session) -> models.User:
    user = db.query(models.User).first()
    if not user:
        user = models.User()
        db.add(user)
        db.commit()
        db.refresh(user)
    return user

@router.get("/today", response_model=schemas.TodayPaperResponse)
async def get_today_paper(db: Session = Depends(get_db)):
    """Return a paper for today.
    For the MVP we simply fetch recent papers from the PubMed client stub and pick the first one.
    In a full implementation we would run the scoring algorithm and avoid repeats.
    """
    user = get_user(db)
    recent = await pubmed_client.fetch_recent_papers(max_results=10)
    if not recent:
        raise HTTPException(status_code=502, detail="Failed to fetch papers from PubMed")
    # Pick first paper that is not already shown to this user today
    paper_data = recent[0]
    # Upsert paper into DB
    paper = db.query(models.Paper).filter_by(pmid=paper_data["pmid"]).first()
    if not paper:
        paper = models.Paper(
            pmid=paper_data["pmid"],
            title=paper_data["title"],
            authors=paper_data.get("authors"),
            journal=paper_data.get("journal"),
            pub_date=paper_data.get("pub_date"),
            abstract=paper_data.get("abstract"),
            url=paper_data.get("url"),
            study_type=paper_data.get("study_type"),
        )
        db.add(paper)
        db.commit()
        db.refresh(paper)
    # Record that this paper was shown today
    user_paper = models.UserPaper(user_id=user.id, paper_id=paper.id)
    db.add(user_paper)
    db.commit()
    # Build a static recommendation reason (MVP placeholder)
    reason = "あなたが家庭医療に関心があるため、最近の臨床実践に役立つランダムな論文を選びました。"
    # Build a static English summary (placeholder)
    summary_en = "This randomized controlled trial evaluates a home‑based intervention for elderly patients, showing improved functional outcomes."
    # Empty related / suggestions for now
    return schemas.TodayPaperResponse(
        paper=schemas.PaperOut.from_orm(paper),
        recommendation_reason=reason,
        summary_en=summary_en,
        related=[],
        suggestions=[],
    )

@router.post("/feedback", status_code=status.HTTP_201_CREATED)
def post_feedback(feedback: schemas.FeedbackCreate, db: Session = Depends(get_db)):
    user = get_user(db)
    paper = db.query(models.Paper).filter_by(pmid=feedback.pmid).first()
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    fb = models.Feedback(user_id=user.id, paper_id=paper.id, feedback_type=feedback.feedback_type)
    db.add(fb)
    db.commit()
    return {"detail": "feedback recorded"}

@router.post("/tomorrow", status_code=status.HTTP_201_CREATED)
def set_tomorrow(topic: schemas.TomorrowTopicCreate, db: Session = Depends(get_db)):
    user = get_user(db)
    tt = db.query(models.TomorrowTopic).filter_by(user_id=user.id).first()
    if tt:
        tt.topic = topic.topic
        tt.set_at = func.now()
    else:
        tt = models.TomorrowTopic(user_id=user.id, topic=topic.topic)
        db.add(tt)
    db.commit()
    return {"detail": "tomorrow topic saved"}

@router.get("/related", response_model=List[schemas.PaperOut])
def get_related(pmid: str, db: Session = Depends(get_db)):
    # Placeholder: return empty list; real implementation would query similar papers
    return []
