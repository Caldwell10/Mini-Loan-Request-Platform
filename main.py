from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import uvicorn

from app.models import User, Loan
from app.schema import UserResponse, UserCreate
from app.database import get_db

app = FastAPI()


@app.get('/')
async def read_root():
    return {"message": "Welcome to the Loan Management API"}


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


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)