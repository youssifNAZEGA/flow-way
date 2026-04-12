from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.deps import get_db
from schemas.auth import RegisterSchema, LoginSchema
from services.auth_services import create_user, authenticate_user
from core.security import create_token,decode_token
from core.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
def register(data: RegisterSchema, db: Session = Depends(get_db)):
    user = create_user(db, data.email, data.password)
    return {
        "message": "User created",
        "User": user
        }

@router.post("/login")
def login(data: LoginSchema, db: Session = Depends(get_db)):
    user = authenticate_user(db, data.email, data.password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # token = create_access_token({"sub": user.email})

    token = create_token(user.email)
    print(token)

    return {
        "message": "Login successful",
        "token": token
    }


@router.get("/me")
def get_me(current_user = Depends(get_current_user)):
    return {
        "email": current_user.email
    }