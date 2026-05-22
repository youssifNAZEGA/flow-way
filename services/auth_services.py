from sqlalchemy.orm import Session
from models.utilisateurs import User
from models.entreprise import Company
from core.security import hash_password, verify_password

def create_user(db: Session, data):
    hashed_password = hash_password(data.password)
    
    user = User(
        email=data.email,
        password=hashed_password,
        firstName=data.firstName,
        lastName=data.lastName,
        role=data.role
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    if data.role == "entreprise" and data.companyName:
        company = Company(
            user_id=user.id,
            name=data.companyName
        )
        db.add(company)
        db.commit()
    
    return user

def authenticate_user(db: Session, email, password):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user
