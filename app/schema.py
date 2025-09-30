from pydantic import BaseModel, Field, EmailStr, condecimal, SecretStr
from typing import Optional
from decimal import Decimal as decimal
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    phone_number: str
    password: str = Field(min_length=8)

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone_number: str

    class Config:
        orm_mode = True

class LoanCreate(BaseModel):
    user_id: int
    amount: condecimal(gt=0, lt=1000000)

class LoanOut(BaseModel):
    id: int
    user_id: int
    amount: decimal
    status: str
    reason: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class WebhookIn(BaseModel):
    loan_id: int
    score: int
    status: str
    reason: str



  
