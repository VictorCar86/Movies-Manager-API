from fastapi import status, HTTPException, APIRouter
from fastapi.responses import JSONResponse
from schemas.user import User
from schemas.generic_response import GenericResponse
from db.config import Session
from utils.jwt_manager import create_token
from models.user import User as UserModel


auth = APIRouter()
db = Session()


@auth.post('/auth/signup', tags=['auth'], response_model=GenericResponse)
def signup(user: User):
	user_exist = db.query(UserModel).\
		filter_by(email= user.email).one_or_none()
	if user_exist:
		raise HTTPException(
			status_code=status.HTTP_403_FORBIDDEN,
			detail='User already exist. Please introduce a valid information'
		)
	db.add( UserModel(**dict(user)) )
	db.commit()
	return JSONResponse(
		status_code=status.HTTP_201_CREATED,
		content={'message': 'Signed up successfully'}
	)

@auth.post('/auth/login', tags=['auth'], response_model=str)
def login(user: User):
	user_exist = db.query(UserModel).\
		filter_by(email= user.email, password= user.password).first()
	if not user_exist:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail='User does not exist.'
		)
	token = create_token({'email': user.email})
	return JSONResponse(content=token)