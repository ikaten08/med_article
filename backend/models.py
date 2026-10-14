# backend/models.py

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    # For MVP we assume a single user – additional auth can be added later
    # Store interests as comma‑separated list (e.g., "Family Medicine,Home Care")
    interests = Column(Text, default="")
    xp = Column(Integer, default=0)
    level = Column(Integer, default=1)
    learning_streak = Column(Integer, default=0)
    last_active = Column(DateTime, default=datetime.utcnow)

    # Relationships
    papers = relationship("UserPaper", back_populates="user")
    feedbacks = relationship("Feedback", back_populates="user")
    tomorrow_topic = relationship("TomorrowTopic", uselist=False, back_populates="user")

class Paper(Base):
    __tablename__ = "papers"
    id = Column(Integer, primary_key=True, index=True)
    pmid = Column(String, unique=True, index=True, nullable=False)
    title = Column(Text, nullable=False)
    authors = Column(Text)
    journal = Column(String)
    pub_date = Column(DateTime)
    abstract = Column(Text)
    url = Column(String)
    study_type = Column(String)  # e.g., "RCT", "Systematic Review"
    fetched_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    users = relationship("UserPaper", back_populates="paper")
    feedbacks = relationship("Feedback", back_populates="paper")

class UserPaper(Base):
    __tablename__ = "user_papers"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    paper_id = Column(Integer, ForeignKey("papers.id"), nullable=False)
    date = Column(DateTime, default=datetime.utcnow)  # when shown as Today’s Paper

    user = relationship("User", back_populates="papers")
    paper = relationship("Paper", back_populates="users")
    __table_args__ = (UniqueConstraint("user_id", "paper_id", name="uq_user_paper"),)

class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    paper_id = Column(Integer, ForeignKey("papers.id"), nullable=False)
    feedback_type = Column(String, nullable=False)  # "interesting", "not_relevant", "already_knew", "save"
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="feedbacks")
    paper = relationship("Paper", back_populates="feedbacks")
    __table_args__ = (UniqueConstraint("user_id", "paper_id", "feedback_type", name="uq_feedback"),)

class TomorrowTopic(Base):
    __tablename__ = "tomorrow_topic"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    topic = Column(Text, nullable=False)
    set_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="tomorrow_topic")
