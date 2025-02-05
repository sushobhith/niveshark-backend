from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, JSON, UUID, Enum, ARRAY, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone
from database import Base
from enum import Enum as PyEnum
import uuid

class InputType(PyEnum):
  RADIO_BUTTON = 'RADIO_BUTTON'
  CHECK_BOX = 'CHECK_BOX'
  INPUT_NUMBER = 'INPUT_NUMBER'
  INPUT_TEXT = 'INPUT_TEXT'

class QuestionCategory(PyEnum):
  FINANCIAL_METRICS = 'FINANCIAL_METRICS'
  INVESTING_POTENTIAL = 'INVESTING_POTENTIAL'
  RISK_TOLERANCE = 'RISK_TOLERANCE'
  RISK_CAPACITY = 'RISK_CAPACITY'

class User(Base):
  __tablename__ = 'users'

  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  username = Column(String(50), unique=True, nullable=False)
  email = Column(String(120), unique=True, nullable=False)
  password_hash = Column(String(128), nullable=False)
  created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
  updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
  
  # Relationships
  responses = relationship("InvestorResponse", back_populates="user")
  financial_metrics = relationship("FinancialMetrics", back_populates="user")
  portfolio_recommendation = relationship("PortfolioRecommendation", back_populates="user")

class Questions(Base):
  __tablename__ = 'questions'

  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  categories = Column(ARRAY(Enum(QuestionCategory, name='question_category', create_type=False)))
  text = Column(Text, nullable=False)  
  input_type = Column(Enum(InputType, name='question_input_type', create_type=False))
  options = Column(JSON, nullable=True)
  weight = Column(JSON, nullable=False)
  display_order = Column(Integer, nullable=False, unique=True)
  # position = Column(String(50), nullable=False)
  created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
  updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

  responses = relationship("InvestorResponse", back_populates="question")

class InvestorResponse(Base):
    __tablename__ = 'investor_responses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    question_id = Column(UUID, ForeignKey('questions.id'), nullable=False)
    # question_id = Column(Integer, nullable=False)  # Maps to predefined questions
    response = Column(String, nullable=False)  # Store as a string
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="responses")
    question = relationship("Questions", back_populates="responses")

class FinancialMetrics(Base):
    __tablename__ = 'financial_metrics'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    
    risk_capacity = Column(Float, nullable=False)  # Calculated Risk Capacity (0-100)
    risk_tolerance = Column(Float, nullable=False)  # Calculated Risk Tolerance (0-100)
    investing_potential = Column(Float, nullable=False)  # Calculated potential investable amount
    liquidity_ratio = Column(Float, nullable=False)  # Liquidity Ratio
    debt_to_income_ratio = Column(Float, nullable=False)  # Debt-to-Income Ratio
    investment_horizon_score = Column(Float, nullable=False)  # Horizon score (0-100)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="financial_metrics")

class PortfolioRecommendation(Base):
    __tablename__ = 'portfolio_recommendations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)

    portfolio_type = Column(String, nullable=False)  # "Conservative", "Aggressive Growth", etc.
    equity_allocation = Column(Float, nullable=False)  # % of equity allocation
    fixed_income_allocation = Column(Float, nullable=False)  # % of fixed-income allocation
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="portfolio_recommendation")