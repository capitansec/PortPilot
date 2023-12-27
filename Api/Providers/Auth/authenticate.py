from Config.database_connector import get_db
from Providers.Cryptology.sha256 import encrypter
from fastapi import HTTPException, Depends
from models import User
from sqlalchemy.orm import Session


async def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    hashed_password = await encrypter(password)
    if hashed_password != user.password:
        raise HTTPException(
            status_code=400,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    print(user.username)
    return user
