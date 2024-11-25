import anyio.from_thread
from robyn.authentication import AuthenticationHandler, BearerGetter, Identity
from robyn import Request, Response
from models import SessionLocal
from utils import fetch_user
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import timedelta, datetime
from sqlalchemy.orm import Session
from log import logger
from typing import Optional
import anyio
import asyncio

pwd_context = CryptContext(schemes=["bcrypt"])
ALGORITHM = "HS256"
SECRET_KEY = "my_secret_key"

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)

def create_access_token(data:dict,expires_delta:timedelta=None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token:str):
    return jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])

# auth for login 
async def authenticate_user(session:Session,username:str,password:str):
    user = await fetch_user(session,username=username)
    if user is None:
        return False
    
    if not verify_password(password,user.get("hashed_password")):
        return False
    
    created_token = create_access_token(data={"sub":user.get("username")})
    return created_token


# auth for routes
class BasicAuthHandler(AuthenticationHandler):

    def __init__(self, token_getter=None):
        self.token_getter = token_getter or BearerGetter()
        self.next_url = None  

        ## overide to redirect or retrurn custom error
        # default is Unauthorised

    # @property
    # def unauthorized_response(self) -> Response:
    #     """
    #     Override the default response when the user is unauthorized.
    #     Instead of a 401 Unauthorized, we redirect the user to the login page.
    #     """

    #     # current_url = self.url_path  # Get the current URL path
    #     # redirect_url = f"/login?next={current_url}"  # Pass the current URL as the 'next' parameter
    #     # logger.info("Redirecting to login...")
    #     # return Response(302, headers={'Location': "/login"}, description="User not logged in. Redirecting to Login")
    
    #     logger.info("Redirecting to login...")

    #     # # If 'next_url' is stored, redirect to login with the 'next' URL
    #     # redirect_url = f"/login?next={self.next_url}" if self.next_url else "/login"
    #     # return Response(302, headers={'Location': redirect_url}, description="Redirecting to Login")
    #     # redirect_url = self.next_url or "/login"
    #     redirect_url="/login"
    #     return Response(302, headers={'Location': redirect_url}, description="User not logged in. Redirecting to Login")


    def authenticate(self, request: Request):
        logger.info("Authenticating user...")
        self.next_url = request.url
        logger.info(f"url is request.url {self.next_url}")
        self.next_url = request.query_params.get("next", "/")  # Default to "/" if no next_url in the query params
        logger.info(f"url is {self.next_url}")

        # Check if the Authorization header is present
        if not request.headers.get("Authorization"):
            logger.info("Authorization token not found in headers")
            return None
        
        token = self.token_getter.get_token(request)

        try:
            # Decode the token
            payload = decode_access_token(token)
            username = payload["sub"]
            logger.info(f"Decoded token is {payload}")

            with SessionLocal() as session:  
                user = anyio.from_thread.run(fetch_user(session, username=username))
                # task = asyncio.create_task(fetch_user(session, username))        
                # user = await task
            if user is None:
                logger.error(f"User not found: {username}")
                return None

            # Return the Identity
            identity = Identity(claims={"user": f"{user}"})
            return identity

        except Exception as e:
            logger.error(f"Error while authenticating: {e}")
            return None
