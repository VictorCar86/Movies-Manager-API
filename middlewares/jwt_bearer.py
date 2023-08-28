from fastapi import Request, status, HTTPException
from fastapi.security import HTTPBearer
from utils.jwt_manager import verify_token

class JWTBearer(HTTPBearer):
	async def __call__(self, request: Request):
		auth = await super().__call__(request)
		verification = verify_token(auth.credentials)
		if verification.get('error'):
			raise HTTPException(
				status_code=status.HTTP_403_FORBIDDEN,
		        detail=verification['error']
		    )