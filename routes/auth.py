from fastapi import status, HTTPException, APIRouter
from fastapi.responses import JSONResponse
from schemas.user import User
from schemas.generic_response import GenericResponse
from utils.jwt_manager import create_token
from models.user import User as UserModel
from services.auth import AuthService


auth = APIRouter()


@auth.post('/auth/signup', tags=['auth'], response_model=GenericResponse)
def signup(user: User):
	user_exist = AuthService().signup_user(user)
	if user_exist:
		raise HTTPException(
			status_code=status.HTTP_403_FORBIDDEN,
			detail='User already exist. Please introduce a valid information'
		)
	return JSONResponse(
		status_code=status.HTTP_201_CREATED,
		content={'message': 'Signed up successfully'}
	)

@auth.post('/auth/login', tags=['auth'], response_model=str)
def login(user: User):
	token = AuthService().login_user(user)
	if not token:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail='User does not exist.'
		)
	return JSONResponse(content=token)