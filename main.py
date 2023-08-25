from fastapi import FastAPI, Depends, Path, Query, status
from fastapi.responses import FileResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from datetime import datetime as dt
from typing import List
from schemas import Movie, GenericResponse, User, JWTBearer
from db import movies, users
from db.config import Session, Base, engine
from jwt_manager import create_token
from models.movie import Movie as MovieModel

app = FastAPI()
app.title = 'TestAPI'
app.version = '0.0.1'
app.description = 'Lorem ipsus'


# Database

Base.metadata.create_all(bind=engine)
db = Session()


# Home

@app.get('/', tags=['home'])
def home():
	return FileResponse('./test/index.html')


# Movies

@app.get('/movies', tags=['movies'], response_model=List[Movie])
def get_movies(
		category: str = Query(default=None, min_length=2, max_length=12),
		year: int = Query(default=None, le=dt.today().year),
	):
	# db = Session()
	if category or year:
		filtered_movies = [ m for m in movies if m['category'] == category or m['year'] == year ]
		return JSONResponse(content=filtered_movies)
	movies = db.query(MovieModel).all()
	return JSONResponse(content=jsonable_encoder(movies))

@app.get('/movies/{id}', tags=['movies'], response_model=Movie)
def get_movie(id: int = Path(ge=1, le=100)):
	result = list( filter(lambda movie: movie['id'] == id, movies) )
	if len(result):
		return JSONResponse(content=result[0])
	raise JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content='Movie not found')

@app.post('/movies', tags=['movies'], response_model=GenericResponse, dependencies=[Depends(JWTBearer())])
def create_movie(movie: Movie):
	new_movie = MovieModel(**dict(movie))
	db = Session()
	db.add(new_movie)
	db.commit()
	response = {'message': 'Movie added successfully', 'movie_id': new_movie.id}
	return JSONResponse(status_code=status.HTTP_201_CREATED, content=response)

@app.put('/movies/{id}', tags=['movies'], response_model=GenericResponse, dependencies=[Depends(JWTBearer())])
def update_movie(movie: Movie, id: int = Path(ge=1, le=100)):
	for item in movies:
		if item['id'] == id:
			item.update(dict(movie))
			return JSONResponse(content={'message': 'Movie modified successfully'})
	raise JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content='Movie not found')

@app.delete('/movies/{id}', tags=['movies'], response_model=GenericResponse, dependencies=[Depends(JWTBearer())])
def delete_movie(id: int = Path(ge=1, le=100)):
	for item in movies:
		if item['id'] == id:
			movies.remove(item)
			return JSONResponse(content={'message': 'Movie deleted successfully'})
	raise JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content='Movie not found')


# Auth

@app.post('/auth/signup', tags=['auth'], response_model=GenericResponse)
def signup(payload: User):
	users.append(payload)
	return JSONResponse(content={'message': 'Signed up successfully'})

@app.post('/auth/login', tags=['auth'], response_model=str)
def login(login: User):
	try:
		users.index(login)
		token = create_token({ 'email': login.email })
		return JSONResponse(content=token)
	except:
		return JSONResponse(content={'error': 'User does not exist.'})