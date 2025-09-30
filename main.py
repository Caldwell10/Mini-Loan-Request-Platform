from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import uvicorn
from sqlalchemy import select, func, exists, update

from app.models import User, Loan
from app.schema import UserResponse, UserCreate, LoanCreate, LoanOut, WebhookIn
from app.database import get_db
from app.services import save_audit_log, hash_password

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
        raise HTTPException(status_code=400, detail="User with this email already exists")

    hashed_password = hash_password(payload.password)

    new_user = User(
        name = payload.name, 
        email = payload.email, 
        phone_number =  payload.phone_number, 
        password = hashed_password
        )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# create a new loan for a user
@app.post('/loan_request/', response_model=LoanOut)
async def create_loan(user_id: int, payload: LoanCreate, db: Session = Depends(get_db)):
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
        
    if has_pending:
        raise HTTPException(status_code=400, detail="User already has a pending loan request")
    
    loan = Loan(
        user_id = payload.user_id,
        amount = payload.amount,
    ) 

    
    db.add(loan)
    db.commit()
    db.refresh(loan)

    # Log the outbound webhook request
    outgoing_payload = {
        "loan_id": loan.id,
        "amount": loan.amount,
        "user": {"name": user.name, "email": user.email},
        "callback_url": "http://localhost:8001/webhook/credit-score"
    }
    save_audit_log(
        db,
        direction="OUTGOING",
        url="http://localhost:8001/credit-score",
        payload=outgoing_payload,
        status_code=0 
    )


    return loan

@app.get('/loan-request/{loan_id}', response_model=LoanOut)
def get_loan(loan_id: int, db: Session = Depends(get_db)):
    loan = db.get(Loan, loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    return loan

@app.post('/webhook/credit-score')
async def receive_credit_score(outgoing_payload: WebhookIn, db: Session = Depends(get_db)):
    loan_id = outgoing_payload.loan_id

    loan = db.get(Loan, loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    
    loan.status = outgoing_payload.status
    loan.reason = outgoing_payload.reason
    db.commit()
    db.refresh(loan)

    # log inbound webhook
    save_audit_log(
        db,
        direction="INBOUND",
        url="http://localhost:8001/webhook/credit-score",
        payload=outgoing_payload.dict(),
        status_code=200
    )
    return loan
    
    
    

    
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)