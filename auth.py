
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from .dependencies import get_current_user
from .database import SessionLocal
from .models import User
from .schemas import UserRegister, UserLogin, UserResponse
from .security import create_access_token


router = APIRouter(prefix="/auth", tags=["Authentication"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register", response_model=UserResponse)
def register(user_data: UserRegister, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(
        User.email == user_data.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    hashed_password = pwd_context.hash(user_data.password)

    new_user = User(
        full_name=user_data.full_name,
        email=user_data.email,
        hashed_password=hashed_password,
        role=user_data.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):

    user = db.query(User).filter(
        User.email == user_data.email
    ).first()

    if not user or not pwd_context.verify(
        user_data.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="Account is inactive"
        )

    access_token = create_access_token(
    data={
        "sub": str(user.id),
        "role": user.role
    }
)

    return {
    "message": "Login successful",
    "access_token": access_token,
    "token_type": "bearer",
    "user_id": user.id,
    "name": user.full_name,
    "role": user.role
}



@router.get("/me", response_model=UserResponse)
def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    return current_user
