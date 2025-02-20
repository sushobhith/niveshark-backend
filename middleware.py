from fastapi import Request
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from logger import logger

import time
import os
import jwt
import json
import redis 

load_dotenv()

r = redis.Redis(host="localhost", port=6379, db=0)

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")

async def add_process_time_header(request: Request, call_next):
  start_time = time.time()
  
  response = await call_next(request)
  
  process_time = time.time() - start_time
  response.headers["X-Process-Time"] = str(process_time)
  
  return response

async def validate_request_json(request: Request, call_next):
  try:
    if request.headers.get('Content-Type') == 'application/json':
      try:
        await request.json()
      except json.JSONDecodeError:
        return JSONResponse(
          status_code=400,
          content={"message": "Invalid JSON format"}
        )
    
    response = await call_next(request)
    return response
      
  except RuntimeError as e:
    if "Body has already been consumed" in str(e):
      return JSONResponse(
        status_code=400,
        content={"message": "Request body has already been consumed"}
      )
    raise

async def validate_jwt_auth(request: Request, call_next):

  path = request.url.path
  # headers = request.headers
  
  # logger.info(f"Incoming request to: {path}")
  body = await request.body()  # Read the request body
  logger.info(f"Incoming request method: {request.method}, URL: {request.url}, Body: {body.decode('utf-8')}")
  # logger.info(f"Incoming request is:  {type(request)}")

  if path.startswith("/auth") and not(path.startswith("/auth/signout")):
    logger.debug("Skipping auth for /auth endpoints")
    return (await call_next(request))
  else:
    token = request.cookies.get("jwt_token")

    if not token:
      return JSONResponse(
            content={"message": "Token not found!"},
            status_code=401
        )
    # token = headers.get("Authorization").replace("Bearer ", "")
    if r.exists(token):
      return JSONResponse(
        content={"message": "User signed out!"},
        status_code=401
      )
    try:
      decoded = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])

      request.state.username = decoded.get('username')
      logger.info(f"Successfully decoded JWT for user: {decoded.get('username')}")
      
      return (await call_next(request))
    except jwt.ExpiredSignatureError:
      logger.warning(f"Expired JWT token attempt for {path}")
      return JSONResponse(
          content={"message": "Token has expired"},
          status_code=401
      )
    except jwt.InvalidTokenError:
      logger.warning(f"Invalid JWT token attempt for {path}")
      return JSONResponse(
          content={"message": "Invalid token"},
          status_code=401
      )