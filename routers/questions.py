from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List, Optional
from logger import logger
from database import get_db
from models import Questions, User, InvestorResponse, FinancialMetrics
from pydantic import BaseModel

router = APIRouter()

# ---------------------------
# Pydantic Schemas
# ---------------------------
class QuestionResponse(BaseModel):
  id: str
  text: str
  input_type: str
  possible_inputs: Optional[List[str]] = None
  display_order:int

  class Config:
    orm_mode = True

class QuestionResponseItem(BaseModel):
  text: str
  response: str
  id: str

class SubmitQuestionnaireRequest(BaseModel):
  submitted_response: str
  question_id: str

class SubmitQuestionnaireResponse(BaseModel):
  message: str
  risk_capacity: int
  risk_tolerance: int
  investing_potential: int
  liquidity_ratio: int
  debt_to_income_ratio: int
  investment_horizon_score: int


# ---------------------------
# Routes
# ---------------------------

@router.get("/", response_model=List[QuestionResponse])
def get_questionnaire(db: Session = Depends(get_db)):
  # Retrieve the entire questionnaire from the DB.
  # Could be protected if only authenticated users can see it.

  questions = db.query(Questions).all()

  questions_response_list = []
  for item in questions:

    value = QuestionResponse(
        id=str(item.id),
        text=item.text,
        input_type=item.input_type.value,
        possible_inputs=item.options,
        display_order=item.display_order
      )
    
    questions_response_list.append(value)

  return questions_response_list


@router.post("/submit", response_model=SubmitQuestionnaireResponse)
def submit_questionnaire(request: Request, payload: List[SubmitQuestionnaireRequest], db: Session = Depends(get_db)):

  user = db.query(User).filter(User.username == request.state.username).first()
  if not user:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Invalid username or password."
    )
  
  investment_type = 0
  investing_potential = 0
  income_stability = 0
  owns_house = 0
  savings_rate = 0
  investment_experience = 0
  fixed_asset_allocation = 0
  portfolio_checking_freq = 0
  market_dip_action = 0
  investment_strategy = 0
  portfolio_crash_reaction = 0 
  investment_horizon = 0
  has_dependents = 0
  liquidity_ratio = 0
  major_financial_goals = 0
  debt_to_income_ratio = 0



  response_list = []
  for item in payload:
    new_response = InvestorResponse(user_id=user.id, question_id=item.question_id, response=item.submitted_response)
    question = db.query(Questions).filter(Questions.id == item.question_id).first()
    
    # 1. Investment Type (SIP vs. One-Time) → Affects Risk Tolerance & Investing Potential
    if question.text == 'How do you want to invest your money?':
      if item.submitted_response == "SIP":
          investment_type = -5
      elif item.submitted_response == "One Time":
          investment_type = 5
      else:
          investment_type = 0  # Default value if neither condition is met

    # 2. Investing Potential → Directly used
    if question.text == 'How much amount do you want to invest?':
      investing_potential = int(item.submitted_response)

    # 3. Income Stability → Affects Risk Capacity
    if question.text == 'How regular is your income?':
      if item.submitted_response == "Regular monthly income":
          income_stability = 10
      elif item.submitted_response == "Irregular monthly income":
          income_stability = 5
      elif item.submitted_response == "No monthly income":
          income_stability = 0
      else:
          income_stability = 0  # Default value if neither condition is met

    # 4. Homeownership → More security = Higher Risk Capacity
    if question.text == 'Do you own a house?':
      owns_house = 5 if item.submitted_response == "Yes" else 0

    # 5. Savings Rate → Affects Risk Capacity
    if question.text == 'What %age of your annual income do you save?':
      if item.submitted_response == "Greater than or equal to 30%":
          savings_rate = 10
      elif item.submitted_response == "Less than 30%":
          savings_rate = 7
      elif item.submitted_response == "Less than 20%":
          savings_rate = 4
      elif item.submitted_response == "Less than 10%":
          savings_rate = 1
      else:
          savings_rate = 0  # Default value if neither condition is met

    # 6. EMI Burden → Affects Debt-to-Income Ratio
    # if question.text == 'What %age of your annual income goes into the EMI?':
    #   if item.submitted_response == "Less than 10%":
    #       emi_burden = 1
    #   elif item.submitted_response == "Less than 20%":
    #       emi_burden = 0.5
    #   elif item.submitted_response == "Less than 40%":
    #       emi_burden = -0.5
    #   elif item.submitted_response == "Greater than 40%":
    #       emi_burden = -1
    #   else:
    #       emi_burden = 0  # Default value if neither condition is met

    # 7. Investment Experience → Affects Risk Capacity
    if question.text == 'What is your investing experience in mutual funds and stocks?':
      if item.submitted_response == "Never invested":
          investment_experience = -10
      elif item.submitted_response == "Started less than 3 years back":
          investment_experience = -5
      elif item.submitted_response == "Investing from last 10 years to 3 years":
          investment_experience = 5
      elif item.submitted_response == "Investing for more than 10 years":
          investment_experience = 10
      elif item.submitted_response == "I have stopped investing":
          investment_experience = -10
      else:
          investment_experience = 0  # Default value if neither condition is met

    # 8. Fixed Asset Allocation → Affects Risk Capacity
    if question.text == 'What %age of your investment is in FD, PPF, NSC etc.?':
      if item.submitted_response == "Less than 20%":
          fixed_asset_allocation = 10
      elif item.submitted_response == "Between 20-30%":
          fixed_asset_allocation = 5
      elif item.submitted_response == "Between 40-50%":
          fixed_asset_allocation = -5
      elif item.submitted_response == "Greater than 60%":
          fixed_asset_allocation = -10
      else:
          fixed_asset_allocation = 0  # Default value if neither condition is met

    # 9. Portfolio Checking Frequency → Affects Risk Tolerance
    if question.text == 'How often do you check your portfolio value?':
      if item.submitted_response == "Everyday":
          portfolio_checking_freq = -10
      elif item.submitted_response == "4 to 5 times a month":
          portfolio_checking_freq = -5
      elif item.submitted_response == "Every month":
          portfolio_checking_freq = 0
      elif item.submitted_response == "4 to 5 times a year":
          portfolio_checking_freq = 5
      else:
          portfolio_checking_freq = 0  # Default value if neither condition is met

    # 10. Market Dip Action → Affects Risk Tolerance
    if question.text == 'In which market dip would you take corrective action?':
      if item.submitted_response == "Portfolio is down 10%":
          market_dip_action = -10
      elif item.submitted_response == "Portfolio is down 20%":
          market_dip_action = -5
      elif item.submitted_response == "Portfolio is down 30%":
          market_dip_action = 0
      elif item.submitted_response == "Portfolio is down more than 40%":
          market_dip_action = 5
      elif item.submitted_response == "None of the above":
          market_dip_action = 10
      else:
          market_dip_action = 0  # Default value if neither condition is met
    
    # 11. Portfolio Strategy → Affects Risk Tolerance
    if question.text == 'What portfolio strategy would you like to have?':
      if item.submitted_response == "Preserve principal amount even if post tax growth is below inflation":
          investment_strategy = -10
      elif item.submitted_response == "Preserve principal amount with post tax growth at par with inflation":
          investment_strategy = -5
      elif item.submitted_response == "Achieve moderate growth":
          investment_strategy = 5
      elif item.submitted_response == "Achieve high growth":
          investment_strategy = 10
      elif item.submitted_response == "Maximise growth":
          investment_strategy = 15
      else:
          investment_strategy = 0  # Default value if neither condition is met

    # 12. Portfolio Crash Reaction → Affects Risk Tolerance
    if question.text == 'What would you do if your portfolio dropped 50%?':
      if item.submitted_response == "Sell everything":
          portfolio_crash_reaction = -10
      elif item.submitted_response == "Hold and wait":
          portfolio_crash_reaction = 5
      elif item.submitted_response == "Invest more":
          portfolio_crash_reaction = 10
      else:
          portfolio_crash_reaction = 0  # Default value if neither condition is met

    # 13. Investment Horizon → Affects Risk Capacity
    if question.text == 'What is your preferred investment horizon?':
      if item.submitted_response == "Less than 3 years":
          investment_horizon = -10
      elif item.submitted_response == "3 to 5 years":
          investment_horizon = 0
      elif item.submitted_response == "More than 5 years":
          investment_horizon = 10
      else:
          investment_horizon = 0  # Default value if neither condition is met

    # 14. Dependents → More dependents = Lower Risk Capacity
    if question.text == 'What is your preferred investment horizon?':
      has_dependents = -10 if item.submitted_response == "Yes" else 0

    # 15. Emergency Savings → Affects Liquidity Ratio
    if question.text == 'How many months of expenses can your emergency savings cover?':
      if item.submitted_response == "Less than 3 months":
          liquidity_ratio = -10
      elif item.submitted_response == "3 to 6 months":
          liquidity_ratio = 0
      elif item.submitted_response == "More than 6 months":
          liquidity_ratio = 10
      else:
          liquidity_ratio = 0  # Default value if neither condition is met

    # 16. Financial Goals → Short-term goals lower risk-taking ability
    if question.text == 'Do you have any significant financial goals in the next 3-5 years?':
      major_financial_goals = -10 if item.submitted_response == "Yes" else 0

    # 17. Additional Income Sources → Increases Investing Potential
    # if question.text == 'Do you have additional sources of income?':
    #   additional_income = 5 if item.submitted_response == "Yes" else 0

    # 18. Personal Loans Taken Recently → Affects Debt-to-Income Ratio
    # if question.text == 'Have you taken any personal loans or high-interest debt in the last year?':
    #   personal_loans = -5 if item.submitted_response == "Yes" else 0

    # 19. EMI Percentage → Affects Debt-to-Income Ratio
    if question.text == 'What percentage of your income goes towards EMIs (Debt-to-Income Ratio)?':
      if item.submitted_response == "Less than 20%":
          debt_to_income_ratio = 10
      elif item.submitted_response == "20-40%":
          debt_to_income_ratio = 0
      elif item.submitted_response == "More than 40%":
          debt_to_income_ratio = -10
      else:
          debt_to_income_ratio = 0  # Default value if neither condition is met

    db.add(new_response)
    db.commit()
    response_list.append(new_response)

  # Final Risk Capacity Calculation
  risk_capacity = (income_stability * 10) + savings_rate + owns_house + investment_experience + \
                  fixed_asset_allocation + has_dependents + major_financial_goals

  # Final Risk Tolerance Calculation
  risk_tolerance = (portfolio_checking_freq + market_dip_action + investment_strategy +
                    portfolio_crash_reaction + investment_type)  
  
  logger.info(f"Scores are :- income_stability = {income_stability}, savings_rate = {savings_rate}, owns_house = {owns_house}\
              , investment_experience = {investment_experience}, fixed_asset_allocation = {fixed_asset_allocation}\
              , has_dependents = {has_dependents}, major_financial_goals = {major_financial_goals}\
              , portfolio_checking_freq = {portfolio_checking_freq}, market_dip_action = {market_dip_action}\
              , investment_strategy = {investment_strategy}, portfolio_crash_reaction = {portfolio_crash_reaction}\
              , investment_type = {investment_type}")
      
  financial_metrics = FinancialMetrics(user_id=user.id, risk_capacity=risk_capacity, risk_tolerance=risk_tolerance, investing_potential=investing_potential, liquidity_ratio=liquidity_ratio, debt_to_income_ratio=debt_to_income_ratio, investment_horizon_score=investment_horizon)
  db.add(financial_metrics)
  db.commit()

  return SubmitQuestionnaireResponse(
    risk_capacity=risk_capacity,
    risk_tolerance=risk_tolerance,
    investing_potential=investing_potential,
    liquidity_ratio=liquidity_ratio,
    debt_to_income_ratio=debt_to_income_ratio,
    investment_horizon_score=investment_horizon,
    message="Ok"
    )