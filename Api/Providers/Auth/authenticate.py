from Config.database_connector import get_db
from Providers.Cryptology.sha256 import encrypter
from fastapi import HTTPException, Depends
from models import User
from sqlalchemy.orm import Session


async def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise InvalidCredentialsException()
    hashed_password = await encrypter(password)
    if hashed_password != user.password:
        raise InvalidCredentialsException()
    return user

class InvalidCredentialsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
