from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List, Optional
from logger import logger
from database import get_db
from models import User, FinancialMetrics, PortfolioRecommendation
from pydantic import BaseModel

router = APIRouter()

# ---------------------------
# Pydantic Schemas
# ---------------------------
class GeneratePortfolioResponse(BaseModel):
  user_id: str
  portfolio_type: str
  equity_allocation: int
  fixed_income_allocation: int

class QuestionResponseItem(BaseModel):
  text: str
  response: str
  id: str


# ---------------------------
# Routes
# ---------------------------
@router.get("/", response_model=GeneratePortfolioResponse)
def generate_portfolio(request: Request, db: Session = Depends(get_db)):

  logger.info(f"Get portfolio attempt for username: {request.state.username}")

  user = db.query(User).filter(User.username == request.state.username).first()
  if not user:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Invalid username or password."
    )

  metrics = db.query(FinancialMetrics).filter_by(user_id=user.id).first()
  if not metrics:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="Please fill the questionnaire!"
    )
  
  final_score = (0.3 * metrics.risk_capacity) + (0.3 * metrics.risk_tolerance) + \
                (0.15 * metrics.investing_potential) + (0.1 * metrics.liquidity_ratio) - \
                (0.1 * metrics.debt_to_income_ratio) + (0.05 * metrics.investment_horizon_score)

  # Determine portfolio type
  if final_score < 30:
      portfolio_type = "Ultra Conservative"
      equity = 20
      fixed_income = 80
  elif final_score < 50:
      portfolio_type = "Conservative"
      equity = 35
      fixed_income = 65
  elif final_score < 70:
      portfolio_type = "Moderate Growth"
      equity = 50
      fixed_income = 50
  elif final_score < 85:
      portfolio_type = "Aggressive Growth"
      equity = 70
      fixed_income = 30
  else:
      portfolio_type = "High Growth"
      equity = 90
      fixed_income = 10

  recommendation = PortfolioRecommendation(
    user_id=user.id,
    portfolio_type=portfolio_type,
    equity_allocation=equity,
    fixed_income_allocation=fixed_income
  )

  db.add(recommendation)
  db.commit()

  logger.info(f"Portfolio generated for username: {request.state.username}")

  return GeneratePortfolioResponse(
    user_id=str(user.id),
    portfolio_type=portfolio_type,
    equity_allocation=equity,
    fixed_income_allocation=fixed_income
    )