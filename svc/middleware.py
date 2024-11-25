
# instead using auth.py 
class Middleware:
    """
    Base Middleware class to define a common structure for all middlewares.
    """
    async def process_request(self, request):
        """
        Method to process the request. Override in subclasses.
        """
        raise NotImplementedError("Subclasses must implement `process_request`.")

from robyn import Request
import logging

logger = logging.getLogger(__name__)

class TokenExtractionMiddleware(Middleware):
    """
    Middleware to extract Bearer token from the Authorization header.
    """

    async def process_request(self, request: Request):
        """
        Extract Bearer token from the Authorization header.
        """
        authorization_header = request.headers.get("authorization")
        if authorization_header and authorization_header.startswith("Bearer "):
            token = authorization_header[7:]  # Extract token
            logger.info(f"Token extracted: {token}")
            request.token = token
        else:
            logger.info("No Bearer token found.")
            request.token = None

from jose import JWTError, jwt

SECRET_KEY = "my_secret_key"
ALGORITHM = "HS256"

class AuthenticationMiddleware(Middleware):
    """
    Middleware for validating Bearer tokens and attaching user identity.
    """

    async def process_request(self, request: Request):
        """
        Validate the Bearer token and attach user identity to the request.
        """
        token = getattr(request, "token", None)
        if not token:
            logger.warning("Token is missing.")
            return {"status_code": 401, "body": "Unauthorized: Missing token"}

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if not username:
                raise JWTError("Token missing 'sub' claim")
            logger.info(f"Token validated for user: {username}")
            request.user_identity = {"username": username}
        except JWTError as e:
            logger.error(f"Invalid token: {e}")
            return {"status_code": 401, "body": "Unauthorized: Invalid token"}

from functools import wraps

class CustomRouter:
    """
    Custom router to process additional route attributes like `need_authentication`.
    """

    def __init__(self, app):
        self.app = app
        self.middlewares = []

    def add_middleware(self, middleware: Middleware):
        """
        Register a middleware.
        """
        self.middlewares.append(middleware)

    def route(self, path, method="GET", **kwargs):
        """
        Custom route decorator to handle additional attributes.
        """
        def decorator(handler):
            @wraps(handler)
            async def wrapped_handler(request: Request):
                # Process middlewares if `need_authentication` is True
                if kwargs.get("need_authentication", False):
                    for middleware in self.middlewares:
                        response = await middleware.process_request(request)
                        if response:  # Middleware returned a response (e.g., unauthorized)
                            return response

                # Execute the actual handler
                return await handler(request)

            # Register the wrapped handler with the app
            self.app.add_route(path, wrapped_handler, method)
            return wrapped_handler

        return decorator
