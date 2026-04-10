from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
import user_models, user_schemas
from database import SessionLocal

SECRET_KEY = "lala"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter(prefix="/auth", tags=["Auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/signup", response_model=user_schemas.UserResponse)
def signup(request: user_schemas.SignupRequest, db: Session = Depends(get_db)):
    # Check if email already exists
    existing_email = db.query(user_models.User).filter(
        user_models.User.email == request.email
    ).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Check if username already exists
    existing_username = db.query(user_models.User).filter(
        user_models.User.username == request.username
    ).first()
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already taken")

    # Create new user
    new_user = user_models.User(
        username=request.username,
        email=request.email,
        hashed_password=hash_password(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login", response_model=user_schemas.TokenResponse)
def login(request: user_schemas.LoginRequest, db: Session = Depends(get_db)):
    user = db.query(user_models.User).filter(
        user_models.User.email == request.email
    ).first()


    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )


    token = create_access_token(data={"sub": user.email, "user_id": user.id})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/forgot-password")
def forgot_password(request: user_schemas.ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(user_models.User).filter(
        user_models.User.email == request.email
    ).first()
    if not user:
        raise HTTPException(status_code=404, detail="No account with that email")

    reset_token = create_access_token(data={"sub": user.email, "purpose": "reset"})
    return {
        "message": "Password reset token generated",
        "reset_token": reset_token  
    }