from app.database import SessionLocal
from app import crud, schemas
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import os
from .secrets.auth_secret import get_secret

secrets = get_secret()
SECRET_KEY = secrets["TASK_MASTER_PRO_AUTH_SECRET_KEY"]
ALGORITHM = "HS256"

# The OAuth2PasswordBearer class is used to create a dependency that can be used to authenticate users.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    # The get_db() function is used to create a new database session for each request.
    db = SessionLocal()
    try:
        # The yield keyword is used to return the database session to the caller.  This allows the caller to use the session to interact with the database.
        yield db
    finally:
        db.close()

# The get_current_user() function is used to retrieve the current user from the database based on the authentication token.
def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    # The credentials_exception variable is used to create an HTTPException that will be raised if the credentials are invalid.
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # The jwt.decode() function is used to decode the authentication token using the SECRET_KEY and ALGORITHM.
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # The email address is extracted from the payload.
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        # The TokenData object is created with the email address.
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    
    user = crud.get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user