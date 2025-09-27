import enum
from database import Base
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, text, func
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email =Column(String, unique=True, index=True, nullable=False)
    phone_number = Column(String, unique=True, index=True, nullable=False)
    loans = relationship("Loan", back_populates="user", cascade="all, delete-orphan")

class Loan(Base):
    __tablename__ = 'loans'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False, index=True)
    amount = Column(Float, nullable=False)
    status = Column(String, nullable=False, server_default='PENDING')
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default = func.now(), nullable=False)
    reason = Column(String, nullable=False, index=True, server_default='Pending review')
    user = relationship("User", back_populates="loans")

class AuditLog(Base):

    __tablename__ = 'audit_logs'

    id = Column(Integer, primary_key=True, index=True)
    direction = Column(String, nullable=False) # inbound or outbound
    url = Column(String, nullable=False) 
    payload = Column(String, nullable=False)
    status_code = Column(Integer, nullable=False)










