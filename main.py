from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from routers.auth import router as auth_router
from routers.portfolio import router as portfolio_router
from routers.questions import router as questions_router
from middleware import add_process_time_header, validate_request_json, validate_jwt_auth
from logger import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up FastAPI application")
    yield
    logger.info("Shutting down FastAPI application")

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost",  # Add your allowed origins here
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods, including OPTIONS
    allow_headers=["*"],  # Allow all headers
)

@app.middleware("http")
async def add_process_time_header_entrypoint(request, call_next):
  return await add_process_time_header(request, call_next)

@app.middleware("http")
async def validate_request_json_entrypoint(request, call_next):
  return await validate_request_json(request, call_next)

@app.middleware("http")
async def validate_jwt_auth_entrypoint(request, call_next):
  return await validate_jwt_auth(request, call_next)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
# app.include_router(finance_router, prefix="/finance", tags=["finance"])
app.include_router(questions_router, prefix="/questions", tags=["questions"])
app.include_router(portfolio_router, prefix="/portfolio", tags=["portfolio"])


