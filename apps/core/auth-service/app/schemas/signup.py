from pydantic import BaseModel, EmailStr, constr

class SignupRequest(BaseModel):
    email: EmailStr
    password: constr(min_length=4)  # ty:ignore[invalid-type-form]

class SignupResponse(BaseModel):
    id: str
    email: EmailStr