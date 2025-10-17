from datetime import datetime
from sqlalchemy import (Column, Integer, String, Boolean, ForeignKey, Text,
                        DateTime)
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

Base = declarative_base()

class FAQ(Base):
    __tablename__ = "faqs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)

class Program(Base):
    __tablename__ = "programs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    description = Column(Text)
    cost = Column(Integer)

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    required = Column(Boolean, default=True)

class Step(Base):
    __tablename__ = "steps"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    step_number = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)

class Candidate(Base):
    __tablename__ = "candidates"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(Integer, unique=True, nullable=False)  # Should be non-nullable for identification
    full_name = Column(Text)
    status = Column(String(50), default="new")
    interactions = relationship("Interaction", back_populates="candidate", cascade="all, delete-orphan")

class Interaction(Base):
    __tablename__ = "interactions"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False)
    user_message = Column(Text)
    bot_response = Column(Text)
    contexts_json = Column(Text)  # Storing context as JSON string
    created_at = Column(DateTime, default=func.now(), nullable=False)
    candidate = relationship("Candidate", back_populates="interactions")
