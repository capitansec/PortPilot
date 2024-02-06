import os

from fastapi import APIRouter, Depends, Security, HTTPException
from Http.Requests.user import UserLoginBase, UserRegisterBase
from Providers.Auth.authenticate import authenticate_user
from Providers.Cryptology.sha256 import encrypter
from Providers.Environment.environment import *
from Middleware.Auth.token import verify_token
from Http.Responses.user import ResponseModel, BaseResponse, UserResponse
from Http.Responses import *
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from Config.redis_connector import RedisConnector
from fastapi.security import HTTPBearer
from Config.database_connector import get_db
from sqlalchemy.orm import Session
from models import User
from uuid import UUID
import jwt
from jwt.exceptions import InvalidSignatureError
from Providers.Log.log_writter import log_writer

router = APIRouter(prefix="/v1")


@router.post("/user/login", tags=["User"])
async def login_user(user: UserLoginBase, db: Session = Depends(get_db)):
    try:
        authenticated_user = await authenticate_user(user.username, user.password, db)

        with RedisConnector() as RedisConnection:
            existing_token = RedisConnection.search_key(authenticated_user.username)
            if existing_token:
                response = BaseResponse(status="failed", message="User already on active session", result="")
                return JSONResponse(status_code=400, content=response.dict())

            jwt_payload = {"username": authenticated_user.username}
            jwt_token = jwt.encode(jwt_payload, SECRET_KEY, algorithm=ALGORITHM)
            expire_seconds = int(ACCESS_TOKEN_EXPIRE_MINUTES) * 60
            RedisConnection.write_index(authenticated_user.username, str(expire_seconds), jwt_token)

        response = BaseResponse(status="success", message="User logged in successfully", result=jwt_token)
        return JSONResponse(status_code=200, content=response.dict())

    except Exception as e:
        log_writer(str(e), "ERROR")
        raise HTTPException(status_code=500, detail="An error occurred")


@router.post("/user/register", tags=["User"])
async def create_user(user: UserRegisterBase, db: Session = Depends(get_db)):
    try:
        hashed_password = await encrypter(user.password)
        db_user = User(
            username=user.username,
            email=user.email,
            password=hashed_password,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        response = BaseResponse(status="success", message="User has been created", result=f"{user.username}")
        return JSONResponse(status_code=200, content=response.dict())

    except IntegrityError as e:
        error_message = str(e.orig)
        if "duplicate key value violates unique constraint" in error_message:
            print(e)
            raise HTTPException(status_code=400, detail="Username or email already exists")
        else:
            print(e)
            raise HTTPException(status_code=400,
                                detail="An error occurred during user registration")  # Diğer IntegrityError'ları işlemek için
    except Exception as e:
        print(e)
        log_writer(str(e), "ERROR")
        raise HTTPException(status_code=400, detail="An error occurred during user registration")


@router.get("/user/logout", tags=["User"])
async def logout_user(Authorization: str = Security(HTTPBearer())):
    try:
        token = Authorization.credentials
        decoded_token = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
        username = decoded_token.get("username")

        with RedisConnector() as RedisConnection:
            redis_token = RedisConnection.search_key(username)
            if redis_token:
                RedisConnection.delete_index(username)
                response = BaseResponse(status="success", message="User logged out", result="")
                return JSONResponse(status_code=200, content=response.dict())

            raise HTTPException(status_code=400, detail="User not logged in")

    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="User not logged in")  # cookie yanlış ya da manipüle edilmeye çalışılıyorsa

    except Exception as e:
        log_writer(str(e), "ERROR")
        raise HTTPException(status_code=400, detail="User not logged out")



@router.get("/user/{uuid}", tags=["User"])
async def get_user(uuid: str, db: Session = Depends(get_db), authenticate: str = Depends(verify_token)):
    try:
        valid_uuid = UUID(uuid)

        if not valid_uuid:
            raise ValueError("Invalid UUID")

        db_user = db.query(User).filter(User.uuid == valid_uuid).first()
        if db_user is None:
            response = BaseResponse(status="failed", message="User not found")
            return JSONResponse(status_code=404, content=response.dict())

        user = UserResponse(
            id=db_user.id,
            uuid=str(db_user.uuid),
            email=db_user.email,
            username=db_user.username,
        )
        response = ResponseModel(status="success", message="User checked", result=[user])
        return JSONResponse(status_code=200, content=response.dict())

    except ValueError as e:
        raise HTTPException(status_code=400, detail="Invalid UUID")

    except Exception as e:
        log_writer(str(e), "ERROR")
        raise HTTPException(status_code=500, detail="An error occurred.")


@router.get("/users", tags=["User"])
async def get_all_users(db: Session = Depends(get_db), authenticate: str = Depends(verify_token)):
    try:
        db_users = db.query(User).all()

        if db_users:
            users = []
            for db_user in db_users:
                user = UserResponse(
                    id=db_user.id,
                    uuid=str(db_user.uuid),
                    email=db_user.email,
                    username=db_user.username,
                )
                users.append(user)

            response = ResponseModel(
                status="success",
                message="Users list",
                result=users
            )
            return JSONResponse(content=response.dict(), status_code=200)

        else:
            response = ResponseModel(status="success", message="No users found", result=[])
            return JSONResponse(content=response.dict(), status_code=404)

    except Exception as e:
        log_writer(str(e), "ERROR")
        response = ResponseModel(status="error", message="An error occurred", result=[])
        return JSONResponse(content=response.dict(), status_code=500)
