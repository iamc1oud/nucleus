from sqlmodel import Field, SQLModel
from datetime import datetime
from typing import Optional

class AuthorizationCode(SQLModel, table=True):
    __tablename__ = "authorization_codes"

    id: Optional[int] = Field(default=None, primary_key=True)
    code: str = Field(unique=True, index=True)
    user_id: str
    client_id: str
    redirect_uri: str
    scope: str
    code_challenge: str
    code_challenge_method: str
    expires_at: datetime = Field(index=True)  # Add index for efficient cleanup queries
    used: bool = Field(default=False, index=True)  # Add index for filtering
    created_at: datetime = Field(default_factory=datetime.now)
