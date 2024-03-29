from Config.redis_connector import RedisConnector
from fastapi.security import HTTPBearer
from fastapi import HTTPException, Depends
from fastapi import Security
import jwt
import os
from Providers.Log.log_writter import log_writer



async def verify_token(Authorization: str = Security(HTTPBearer())):
    try:
        if not Authorization:
            raise HTTPException(status_code=403, detail="No authorization provided")

        token = Authorization.credentials # jwt payload

        decoded_token = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
        username = decoded_token.get("username")
        if username:
            with RedisConnector() as RedisConnection:
                if not RedisConnection.search_key(username):
                    raise HTTPException(status_code=401, detail="Token expired or invalid")

        else:
            raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=403, detail="Invalid Token")


async def get_current_user(credentials: HTTPBearer = Security(HTTPBearer())):
    try:
        if not credentials:
            raise HTTPException(status_code=403, detail="No authorization provided")

        token = credentials.credentials
        decoded_token = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
        username = decoded_token.get("username")
        if username:
            return username
        else:
            raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        log_writer(str(e), "ERROR")
        raise HTTPException(status_code=500, detail="Error while getting user.")
