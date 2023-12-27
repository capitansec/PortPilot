from fastapi import FastAPI, Depends
from Http.Routes import user, scan
from Middleware.Auth.token import verify_token
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.include_router(user.router)
app.include_router(scan.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)