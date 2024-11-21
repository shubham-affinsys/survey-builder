from robyn.authentication import AuthenticationHandler, BearerGetter, Identity
from robyn import Request, Response
from models import SessionLocal
from utils import fetch_user
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import timedelta, datetime
from sqlalchemy.orm import Session
from log import logger


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


def authenticate_user(session:Session,username:str,password:str):
    user = fetch_user(session,username)
    if user is None:
        return False
    
    if not verify_password(password,user.get("hashed_password")):
        return False
    
    created_token = create_access_token(data={"sub":user.get("username")})
    return created_token


class BasicAuthHandler(AuthenticationHandler):
    def __init__(self, token_getter=None):
        # Use the provided token_getter or default to BearerGetter
        self.token_getter = token_getter or BearerGetter()

    @property
    def unauthorized_response(self) -> Response:
        """
        Override the default response when the user is unauthorized.
        Instead of a 401 Unauthorized, we redirect the user to the login page.
        """
        logger.info("redirecting to login...")
        return Response(302, headers={'Location': "/login"},description="User not logged in Redirecting to Login")
    
    def authenticate(self, request):
        logger.info("authenticating user...")
        if not request.headers.get("Authorization"):
            logger.info("Autherization token not found in headers")
            return None
        
        token = self.token_getter.get_token(request)
        try:
            payload = decode_access_token(token)
            username = payload["sub"]
            logger.info(f"decoded token is {payload}")
       
            with SessionLocal() as session:
                user = fetch_user(session,username=username)
            identity  = Identity(claims={"user":f"{user}"})
            return identity
        
        except Exception as e:
            logger.error(f"Error while authentication {e}")
            return None
