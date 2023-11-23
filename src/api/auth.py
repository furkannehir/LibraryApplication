from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt
from typing import Optional
from datetime import datetime, timedelta
from models import User, session

# Secret key for JWT token
SECRET_KEY = "my_beautiful_secret_key"
ALGORITHM = "HS256"

# Token expiration time (e.g., 24 hours)
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

# Create a Password Context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2PasswordBearer for token retrieval
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Token creation function
def createAccessToken(data: dict, expires_delta: Optional[int] = None):
    to_encode = data.copy()
    # if expires_delta:
    #     expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    # else:
    #     expire = datetime.utcnow() + timedelta(minutes=15)
    # to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Verify user credentials (authentication)
def verifyUserCredentials(username: str, password: str):
    user = session.query(User).filter(User.username == username).first()
    if user is None or not pwd_context.verify(password, user.hashed_password):
        return None
    return user

# Authenticate and generate tokens
def authenticateUser(username: str, password: str):
    user = verifyUserCredentials(username, password)
    if user is None:
        return None
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = createAccessToken(data={"sub": username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

# Get current user
def getCurrentUser(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=400, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = session.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=400, detail="User not found")
    return user
