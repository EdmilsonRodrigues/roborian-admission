from fastapi import APIRouter, Depends, HTTPException
from jose import JWTError, jwt
from datetime import datetime, timedelta
from ..db import get_db
from passlib.context import CryptContext
import load_dotenv
from os import getenv

router = APIRouter()
load_dotenv.load_dotenv()

# JWT settings
SECRET_KEY = getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# CryptContext for hashing and verifying passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Function to create access token (JWT)
def create_access_token(email: str) -> str:
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now() + expires_delta
    to_encode = {"exp": expire, "sub": email}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Function to verify password hash
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Function to get user by email (for authentication)
async def _get_user(email: str, db=Depends(get_db)):
    user_data = await db.users.find_one({"email": email})
    return user_data


# Route to generate JWT token
@router.post("/token")
async def login_for_access_token(email: str, password: str, db=Depends(get_db)):
    user = await _get_user(email, db)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    if not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    access_token = create_access_token(email)
    return {"access_token": access_token, "token_type": "bearer"}


# Route to decrypt JWT token
@router.post("/decrypt-token")
async def decrypt_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        return {"email": email}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
