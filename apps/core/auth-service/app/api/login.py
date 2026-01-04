from sqlmodel import Session, select
from fastapi import APIRouter, Depends, HTTPException, Body, Response
from ..database import get_session
from ..models import User
from ..security.password import verify_password
from ..security.session import create_session

router = APIRouter()


@router.post("/login")
def login(
    response: Response,
    email: str = Body(...),
    password: str = Body(...),
    session: Session = Depends(get_session),
):
    user = session.exec(
        statement=select(User).where(User.email == email)
    ).first()

    if not user or not verify_password(user.password_hash, password):
        raise HTTPException(status_code=401, detail="invalid_credential")
    
    session_token = create_session(str(user.id))

    response.set_cookie(
        key="nucleus_session",
        value=session_token,
        httponly=True,
        secure=True,
        samesite="lax"
    )
    
    # return {
    #     "user_id": str(user.id),
    #     "email": user.email,
    #     "email_verified": user.email_verified
    # }
    return {
        "status": "ok"
    }