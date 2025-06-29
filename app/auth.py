from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import HTTPException, status
from app.config import Config

security = HTTPBasic()

def authenticate_user(credentials: HTTPBasicCredentials):
    user = Config.USER_DB.get(credentials.username)
    if not user or credentials.password != user["password"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return {
        "username": credentials.username,
        "role": user["role"],
        "access": Config.ROLE_ACCESS[user["role"]]
    }