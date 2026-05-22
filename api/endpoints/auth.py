from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.deps import get_db
from schemas.auth import RegisterSchema, LoginSchema
from services.auth_services import create_user, authenticate_user
from core.security import create_access_token, create_refresh_token, decode_token
from core.dependencies import get_current_user
from jose import JWTError

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
def register(data: RegisterSchema, db: Session = Depends(get_db)):
    user = create_user(db, data)
    return {
        "message": "User created",
        "user": user
        }

@router.post("/login")
def login(data: LoginSchema, db: Session = Depends(get_db)):
    user = authenticate_user(db, data.email, data.password)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(user.email)
    refresh_token = create_refresh_token(user.email)

    return {
        "message": "Login successful",
        "accessToken": access_token,
        "refreshToken": refresh_token,
        "user": user
    }

@router.post("/refresh")
def refresh(refresh_token: str, db: Session = Depends(get_db)):
    try:
        payload = decode_token(refresh_token)
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
        
        email = payload.get("sub")
        new_access_token = create_access_token(email)
        return {"accessToken": new_access_token}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

@router.post("/logout")
def logout(current_user = Depends(get_current_user)):
    # In a real app, we might blacklist the token
    return {"message": "Successfully logged out"}

@router.get("/profile")
def get_profile(current_user = Depends(get_current_user)):
    return current_user