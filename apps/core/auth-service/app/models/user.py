from datetime import datetime
import uuid
from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    __tablename__ = "users"


    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(index=True, nullable=False)
    password_hash: str
    email_verified: bool = False
    created_at: datetime  = Field(default_factory=datetime.now)
    