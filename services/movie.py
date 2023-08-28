from schemas.movie import Movie
from models.movie import Movie as MovieModel
from db.config import Session

class MovieService:
    def __init__(self) -> None:
        self.db = Session()

    def get_movies(self, category: str, year: str) -> Movie:
        movies = self.db.query(MovieModel)
        if category or year:
            if category:
                movies = movies.filter_by(category= category)
            if year:
                movies = movies.filter_by(year= year)
        return movies.all()

    def get_movie(self, id: int) -> Movie | None:
        return self.db.query(MovieModel).filter_by(id= id).one_or_none()

    def create_movie(self, movie: Movie) -> Movie:
        new_movie = MovieModel(**dict(movie))
        self.db.add(new_movie)
        self.db.commit()
        return new_movie

    def modify_movie(self, id: int, movie: Movie) -> bool:
        movie_filter = self.db.query(MovieModel).filter_by(id= id)
        if not movie_filter.one_or_none():
            return False
        movie_filter.update(dict(movie), synchronize_session='evaluate')
        self.db.commit()
        return True

    def delete_movie(self, id: int) -> bool:
        movie = self.get_movie(id= id)
        if not movie:
            return False
        self.db.delete(movie)
        self.db.commit()
        return True