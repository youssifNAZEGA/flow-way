from pydantic import BaseModel, EmailStr
from typing import Optional

class RegisterSchema(BaseModel):
    email: EmailStr
    password: str
    firstName: str
    lastName: str
    role: str
    companyName: Optional[str] = None

class LoginSchema(BaseModel):
    email: EmailStr
    password: str
