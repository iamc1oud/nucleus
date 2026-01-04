"""
Database utility functions for SQLModel operations
"""
from sqlmodel import Session, select
from .database import get_engine
from .models.oauth import AuthorizationCode
from datetime import datetime

def cleanup_expired_codes():
    """Remove expired authorization codes from database"""
    engine = get_engine()
    with Session(engine) as session:
        statement = select(AuthorizationCode).where(
            AuthorizationCode.expires_at < datetime.now()
        )
        expired_codes = session.exec(statement).all()
        
        for code in expired_codes:
            session.delete(code)
        
        session.commit()
        return len(expired_codes)

def get_active_codes_count():
    """Get count of active (non-expired, unused) authorization codes"""
    engine = get_engine()
    with Session(engine) as session:
        statement = select(AuthorizationCode).where(
            AuthorizationCode.expires_at > datetime.now(),
            AuthorizationCode.used == False
        )
        codes = session.exec(statement).all()
        return len(codes)