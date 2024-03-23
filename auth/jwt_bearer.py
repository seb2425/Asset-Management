from fastapi import Request, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from auth.jwt_handler import decode_jwt
from jwt.exceptions import DecodeError
import importlib

class jwtBearer(HTTPBearer):
    def __init__(self, autoError: bool = True):
        super(jwtBearer, self).__init__(auto_error=autoError)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(jwtBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Invalid or expired token")
            if not await self.verify_jwt(credentials.credentials):
                raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Invalid or expired token")
            return credentials.credentials
        else:
            raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Invalid or expired token")

    async def verify_jwt(self, jwttoken: str):
        isTokenValid = False
        try:
            payload = await decode_jwt(jwttoken)
            if payload:
                main = importlib.import_module('main')
                user_exists = await main.check_user_exists(payload.get("userID"))
                if user_exists:
                    isTokenValid = True
            return isTokenValid
        except:
            raise(HTTPException(status.HTTP_401_UNAUTHORIZED,detail="invalid or expired token"))