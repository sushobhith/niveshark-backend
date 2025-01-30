from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from logger import logger

from database import get_db
from models import Questions 
from pydantic import BaseModel

router = APIRouter()

# ---------------------------
# Pydantic Schemas
# ---------------------------
class QuestionResponse(BaseModel):
  question_text: str
  input_type: str
  possible_inputs: Optional[List[str]] = None
  position:int

  class Config:
    orm_mode = True

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
        question_text=item.question_text,
        input_type=item.question_type.value,
        possible_inputs=item.possible_answers,
        position=item.position
      )
    
    questions_response_list.append(value)

  return questions_response_list
