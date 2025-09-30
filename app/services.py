from app.models import AuditLog
from app.database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from json import dumps
import bcrypt
import json


def save_audit_log(db: Session, *, direction: str, url: str, payload: dict | None, status_code: int) -> None:
    """Save an audit log entry to the database."""
    audit_log = AuditLog(
        direction=direction,
        url=url,
        payload=json.dumps(payload) if payload is not None else None,
        status_code=status_code
    )
    db.add(audit_log)
    db.commit()
    db.refresh(audit_log)

def hash_password(password: str) -> str:
    """Hash a password for storing"""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password