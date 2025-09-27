from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import uvicorn
from sqlalchemy import select, func, exists

from app.models import User, Loan
from app.schema import UserResponse, UserCreate, LoanCreate, LoanOut
from app.database import get_db

app = FastAPI()


@app.get('/')
async def read_root():
    return {"message": "Welcome to the Loan Management API"}

# create a new user
@app.post('/users', response_model=UserResponse)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    # check if user exists
    existing_user = db.query(User).filter((User.email == payload.email))
    if existing_user.first():
        return HTTPException(status_code=400, detail="User with this email already exists")
    new_user = User(**payload.dict())
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# create a new loan for a user
@app.post('/loan_request/{user_id}', response_model=LoanOut)
def create_loan(user_id: int, payload: LoanCreate, db: Session = Depends(get_db)):
    # check if user exists
    user =db.query(User).filter(User.id ==user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # validate amount
    amount = payload.amount
    if amount <= 0 or amount > 1000000:
        raise HTTPException(status_code=400, detail="Amount must be between 0 and 1,000,000")
    
    # reject multiple pending loan requests
    has_pending = db.scalar(
        select(
            exists().where(
                Loan.user_id == payload.user_id , 
                Loan.status == 'PENDING')
                )
    )
    loan = Loan(
        user_id = payload.user_id,
        amount = payload.amount,
    )     
    if has_pending:
        raise HTTPException(status_code=400, detail="User already has a pending loan request")

    
    db.add(loan)
    db.commit()
    db.refresh(loan)

    return loan


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

