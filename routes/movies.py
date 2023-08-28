from fastapi import Depends, Path, Query, status, HTTPException, APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from datetime import datetime as dt
from schemas.movie import Movie
from schemas.generic_response import GenericResponse
from middlewares.jwt_bearer import JWTBearer
from services.movie import MovieService


movies = APIRouter()


@movies.get('/movies', tags=['movies'], response_model=list[Movie])
def get_movies(
		category: str = Query(default=None, min_length=2, max_length=12),
		year: int = Query(default=None, le=dt.today().year),
	):
	movies = MovieService().get_movies(category= category, year= year)
	if not movies:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail='Movies not found'
		)
	return JSONResponse(content=jsonable_encoder(movies))

@movies.get('/movies/{id}', tags=['movies'], response_model=Movie)
def get_movie(id: int = Path(ge=1, le=100)):
	movie = MovieService().get_movie(id= id)
	if not movie:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail='Movie not found'
		)
	return JSONResponse(content=jsonable_encoder(movie))

@movies.post('/movies', tags=['movies'], response_model=GenericResponse, dependencies=[Depends(JWTBearer())])
def create_movie(movie: Movie):
	new_movie = MovieService.create_movie(movie= movie)
	response = {'message': 'Movie added successfully', 'movie_id': new_movie.id}
	return JSONResponse(
		status_code=status.HTTP_201_CREATED,
		content=response
	)

@movies.put('/movies/{id}', tags=['movies'], response_model=GenericResponse, dependencies=[Depends(JWTBearer())])
def update_movie(movie: Movie, id: int = Path(ge=1, le=100)):
	movie_modified = MovieService().modify_movie(id= id, movie= movie)
	if not movie_modified:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail='Movie not found'
		)
	return JSONResponse(content={'message': 'Movie modified successfully'})

@movies.delete('/movies/{id}', tags=['movies'], response_model=GenericResponse, dependencies=[Depends(JWTBearer())])
def delete_movie(id: int = Path(ge=1, le=100)):
	movie_deleted = MovieService().delete_movie(id= id)
	if not movie_deleted:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail='Movie not found'
		)
	return JSONResponse(content={'message': 'Movie deleted successfully'})