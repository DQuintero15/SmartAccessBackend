import secrets
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from src.config.settings import get_settings

app = FastAPI()

security = HTTPBasic()


def verify_basic_session(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    
    print(f"credentials: {credentials}")
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = get_settings().basic_auth_user.encode("utf8")
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = get_settings().basic_auth_password.encode("utf8")
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.get("/users/me")
def read_current_user(username: Annotated[str, Depends(verify_basic_session)]):
    return {"username": username}