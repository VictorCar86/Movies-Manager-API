from pydantic import BaseModel, Field
from datetime import datetime as dt
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from jwt_manager import create_token, verify_token

class Movie(BaseModel):
	title: str = Field(min_length=2, max_length=15)
	overview: str = Field(min_length=15, max_length=50)
	year: int = Field(le=dt.today().year)
	rating: float = Field(default=None, ge=1, le=10)
	category: str = Field(min_length=5, max_length=15)

	model_config = {
		"json_schema_extra": {
			"example": {
				"title": "Mi película",
				"overview": "Descripción de la película",
				"year": dt.today().year,
				"rating": 9.8,
				"category" : "Acción"
			}
		}
	}

class User(BaseModel):
	email: str = Field(min_length=5, max_length=30)
	password: str = Field(min_length=8)

class JWTBearer(HTTPBearer):
	async def __call__(self, request: Request):
		auth = await super().__call__(request)
		verification = verify_token(auth.credentials)
		if verification.get('error'):
			raise JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content=verification)

class GenericResponse(BaseModel):
	message: str