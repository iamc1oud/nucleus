from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from ..database import get_session
from app.models.user import User
from app.security.password import hash_password
from app.schemas.signup import SignupRequest, SignupResponse

router = APIRouter()

@router.post("/signup", response_model=SignupResponse, status_code=201)
def signup(
    payload: SignupRequest,
    session: Session = Depends(get_session),
):
    # Check if user already exists
    existing_user = session.exec(
        select(User).where(User.email == payload.email)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="email_already_registered"
        )

    user = User(
        email=payload.email,
        password_hash=hash_password(payload.password),
    )

    session.add(user)
    try:
        session.commit()
        session.refresh(user)
    except IntegrityError:
        # Fallback in case of race condition
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="email_already_registered"
        )

    return SignupResponse(
        id=str(user.id),
        email=user.email
    )
