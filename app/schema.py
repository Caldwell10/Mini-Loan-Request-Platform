from pydantic import BaseModel, Field, EmailStr, condecimal
from typing import Optional
from models import LoanStatus

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    phone_number: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone_number: str

    class Config:
        orm_mode = True

class LoanCreate(BaseModel):
    userid: int
    amount: condecimal(gt=0, lt=1000000)

class LoanOut(BaseModel):
    id: int
    user_id: int
    amount: float
    status: LoanStatus
    reason: str
    created_at: str
    updated_at: str

    class Config:
        orm_mode = True

class WebhookPayload(BaseModel):
    loan_id: int
    score: int
    status: LoanStatus
    reason: Optional[str] = None



  
