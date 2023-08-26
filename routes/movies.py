from fastapi import Depends, Path, Query, status, HTTPException, APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from datetime import datetime as dt
from schemas.movie import Movie
from schemas.generic_response import GenericResponse
from middlewares.jwt_bearer import JWTBearer
from db.config import Session
from models.movie import Movie as MovieModel


movies = APIRouter()
db = Session()


@movies.get('/movies', tags=['movies'], response_model=list[Movie])
def get_movies(
		category: str = Query(default=None, min_length=2, max_length=12),
		year: int = Query(default=None, le=dt.today().year),
	):
	if category or year:
		filtered_movies = db.query(MovieModel)
		if category:
			filtered_movies = filtered_movies.filter_by(category= category)
		if year:
			filtered_movies = filtered_movies.filter_by(year= year)
		return JSONResponse(content=jsonable_encoder(filtered_movies.all()))
	movies = db.query(MovieModel).all()
	if not movies:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail='Movies not found'
		)
	return JSONResponse(content=jsonable_encoder(movies))

@movies.get('/movies/{id}', tags=['movies'], response_model=Movie)
def get_movie(id: int = Path(ge=1, le=100)):
	result = db.query(MovieModel).filter_by(id= id).one_or_none()
	if not result:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail='Movie not found'
		)
	return JSONResponse(content=jsonable_encoder(result))

@movies.post('/movies', tags=['movies'], response_model=GenericResponse, dependencies=[Depends(JWTBearer())])
def create_movie(movie: Movie):
	new_movie = MovieModel(**dict(movie))
	db.add(new_movie)
	db.commit()
	response = {'message': 'Movie added successfully', 'movie_id': new_movie.id}
	return JSONResponse(status_code=status.HTTP_201_CREATED, content=response)

@movies.put('/movies/{id}', tags=['movies'], response_model=GenericResponse, dependencies=[Depends(JWTBearer())])
def update_movie(movie: Movie, id: int = Path(ge=1, le=100)):
	movie_filter = db.query(MovieModel).filter_by(id= id)
	if not movie_filter.one_or_none():
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail='Movie not found'
		)
	movie_filter.update(dict(movie), synchronize_session='evaluate')
	db.commit()
	return JSONResponse(content={'message': 'Movie modified successfully'})

@movies.delete('/movies/{id}', tags=['movies'], response_model=GenericResponse, dependencies=[Depends(JWTBearer())])
def delete_movie(id: int = Path(ge=1, le=100)):
	movie = db.query(MovieModel).filter_by(id= id).one_or_none()
	if not movie:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail='Movie not found'
		)
	db.delete(movie)
	db.commit()
	return JSONResponse(content={'message': 'Movie deleted successfully'})