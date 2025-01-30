from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, JSON, UUID, Enum, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone
from database import Base
from enum import Enum as PyEnum
import uuid

class QuestionType(PyEnum):
  RADIO_BUTTON = 'RADIO_BUTTON'
  CHECK_BOX = 'CHECK_BOX'
  INPUT_NUMBER = 'INPUT_NUMBER'
  INPUT_TEXT = 'INPUT_TEXT'


class User(Base):
  __tablename__ = 'users'

  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  username = Column(String(50), unique=True, nullable=False)
  email = Column(String(120), unique=True, nullable=False)
  password_hash = Column(String(128), nullable=False)
  created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
  updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
  
  # Relationships
  financial_details = relationship("UserFinancialDetails", back_populates="user", uselist=False)

class Questions(Base):
  __tablename__ = 'questions'

  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  question_text = Column(String(2000), nullable=False)
  question_type = Column(Enum(QuestionType, name='question_type', create_type=False))
  possible_answers = Column(ARRAY(String))
  position = Column(String(50), nullable=False)
  created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
  updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
  
class UserFinancialDetails(Base):
  __tablename__ = 'user_financial_details'

  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  user_id = Column(Integer, ForeignKey('users.id'), unique=True, nullable=False)
  risk_profile = Column(String(50), nullable=True)
  investment_data = Column(JSON, nullable=False)
  created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
  updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
  
  # Relationship
  user = relationship("User", back_populates="financial_details")