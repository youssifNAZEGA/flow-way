# db/security.py
# from fastapi import Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from db.deps import get_db
# from models import Utilisateur

# def require_manager_role(current_user: Utilisateur = Depends(get_current_user)):
#     """BF-058: Vérifier que l'utilisateur est gestionnaire ou admin"""
#     if current_user.role not in ["admin", "gestionnaire"]:
#         raise HTTPException(
#             status_code=403, 
#             detail="Accès réservé aux gestionnaires ou administrateurs"
#         )
#     return current_user



# db/security.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime, timedelta
import os

from db.deps import get_db
from models.utilisateurs import User

# Configuration JWT (à mettre dans .env en production)
SECRET_KEY = os.getenv("SECRET_KEY", "ta-cle-secrete-tres-longue-et-securisee-change-moi")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Créer un token JWT"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, db: Session) -> User | None:
    """Vérifier et décoder un token JWT"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            return None
    except JWTError:
        return None
    
    user = db.query(User).filter(User.id == user_id).first()
    return user


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Dépendance: Récupérer l'utilisateur connecté depuis le token JWT
    BF-003: Authentification sécurisée
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token d'authentification invalide",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    user = verify_token(token, db)
    if user is None:
        raise credentials_exception
    if not user.actif:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Compte désactivé"
        )
    return user


def require_manager_role(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    BF-058: Vérifier que l'utilisateur est gestionnaire ou admin
    """
    if current_user.role not in ["admin", "gestionnaire"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Accès réservé aux gestionnaires ou administrateurs"
        )
    return current_user


def get_password_hash(password: str) -> str:
    """Hacher un mot de passe"""
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Vérifier un mot de passe"""
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.verify(plain_password, hashed_password)