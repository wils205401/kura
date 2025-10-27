from datetime import datetime, timedelta, timezone
from typing import Annotated, Literal

import socket
from fastapi import FastAPI, Depends, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field

import jwt
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash

from app.routers import vision

app = FastAPI(title="Kura API")

# Detect local IP dynamically
def get_local_ip():
    """Return the LAN IP of the current machine."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Does not have to be reachable, just get the local IP
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = "127.0.0.1"
    finally:
        s.close()

    return local_ip

local_ip = get_local_ip()

origins = [
    # "exp://localhost",  # expo go
    # "exp://192.168.1.37:8081", # expo go mobile metro bundler (local ip adress + port)
    f"exp://{local_ip}:8081",  # expo go mobile metro bundler (dynamic local ip address + port)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(vision.router)


# fake_users_db = {
#     "johndoe": {
#         "username": "johndoe",
#         "full_name": "John Doe",
#         "email": "johndoe@example.com",
#         "hashed_password": "$argon2id$v=19$m=65536,t=3,p=4$wagCPXjifgvUFBzq4hqe3w$CYaIb8sB+wtD+Vu/P4uod1+Qof8h+1g7bbDlBID48Rc",
#         "disabled": False,
#     }
# }
# SECRET_KEY = "35db35ebc138d35e95db160fae363b661bbd97a5c60e83464c8af3a27ca7aeba"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

# class Token(BaseModel):
#     access_token: str
#     token_type: str

# class TokenData(BaseModel):
#     username: str | None = None

# class User(BaseModel):
#     username: str
#     email: str | None = None
#     full_name: str | None = None
#     disabled: bool | None = None

# class UserInDB(User):
#     hashed_password: str

# password_hash = PasswordHash.recommended()
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# def verify_password(plaintext_password, hashed_password):
#     return password_hash.verify(plaintext_password, hashed_password)

# def get_password_hash(plaintext_password):
#     return password_hash.hash(plaintext_password)

# def get_user(db, username: str):
#     if username in db:
#         user_dict = db[username]

#         return UserInDB(**user_dict)

# def authenticate_user(db, username: str, password: str):
#     user = get_user(db, username)
#     if not user:
#         return False
#     if not verify_password(password, user.hashed_password):
#         return False
    
#     return user

# def create_access_token(data: dict, expires_delta: timedelta | None = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.now(timezone.utc) + expires_delta
#     else:
#         expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

#     return encoded_jwt

# async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
#     credentials_exception =  HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Could not validate credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         token_data = TokenData(username=username)
#     except InvalidTokenError:
#         raise credentials_exception
    
#     user = get_user(fake_users_db, username=token_data.username)
#     if user is None:
#         raise credentials_exception
    
#     return user

# async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactivate User")
    
#     return current_user

# @app.post("/token")
# async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
#     user = authenticate_user(fake_users_db, form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
    
#     access_token_expires = timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )

#     return Token(access_token=access_token, token_type="bearer")

# @app.get("/users/me/", response_model=User)
# async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
#     return current_user

# @app.get("/users/me/items/")
# async def read_own_items(current_user: Annotated[User, Depends(get_current_active_user)]):
#     return [{"item_id": "Foo", "owner": current_user.username}]

@app.get("/")
async def root():
    return {
        "message:" : "Kura API is running",
        "local_ip": local_ip,
        "allowed_origins": origins,
    }





