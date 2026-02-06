from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import bcrypt
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from . import database, models, schemas
import logging

# Set up logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# SECURITY CONFIGURATION
SECRET_KEY = "your-secret-key-CHANGE-THIS-IN-PRODUCTION"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

router = APIRouter(prefix="/auth", tags=["auth"])

def verify_password(plain_password, hashed_password):
    try:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception:
        return False

def get_password_hash(password):
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(pwd_bytes, salt)
    return hashed_password.decode('utf-8')

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    
    user = db.query(models.User).filter(models.User.email == token_data.email).first()
    if user is None:
        raise credentials_exception
    return user

# --- Routes ---

@router.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    try:
        # Check if email exists
        db_user = db.query(models.User).filter(models.User.email == user.email).first()
        if db_user:
            return JSONResponse(
                status_code=409,  # Conflict
                content={"success": False, "message": "Email already exists"}
            )
        
        # Create new user
        hashed_password = get_password_hash(user.password)
        new_user = models.User(
            email=user.email,
            name=user.name,
            hashed_password=hashed_password
        )
        db.add(new_user)
        try:
            db.commit()
            db.refresh(new_user)
        except Exception:
            db.rollback()
            raise

        return JSONResponse(
            status_code=201,  # Created
            content={"success": True, "message": "Account created successfully"}
        )

    except ValueError as ve:
        # Pydantic validation error (manually raised if any)
        return JSONResponse(
            status_code=400,
            content={"success": False, "message": str(ve)}
        )
    except SQLAlchemyError as e:
        logger.error(f"Database error during registration: {str(e)}")
        return JSONResponse(
            status_code=500, 
            content={"success": False, "message": "Database service unavailable"}
        )
    except Exception as e:
        logger.error(f"Unexpected error during registration: {str(e)}")
        return JSONResponse(
            status_code=500, 
            content={"success": False, "message": "Internal server error"}
        )

@router.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(database.get_db)):
    try:
        # Check if user exists
        db_user = db.query(models.User).filter(models.User.email == user.email).first()
        
        # Verify password (safely handle user not found)
        if not db_user or not verify_password(user.password, db_user.hashed_password):
            return JSONResponse(
                status_code=401, 
                content={"success": False, "message": "Invalid email or password"}
            )
        
        # Generate token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": db_user.email}, expires_delta=access_token_expires
        )
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True, 
                "message": "Login successful",
                "access_token": access_token, 
                "token_type": "bearer"
            }
        )

    except SQLAlchemyError as e:
        logger.error(f"Database error during login: {str(e)}")
        return JSONResponse(
            status_code=500, 
            content={"success": False, "message": "Database service unavailable"}
        )
    except Exception as e:
        logger.error(f"Unexpected error during login: {str(e)}")
        return JSONResponse(
            status_code=500, 
            content={"success": False, "message": "An unexpected error occurred"}
        )

@router.get("/me", response_model=schemas.UserResponse)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user
