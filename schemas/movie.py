from pydantic import BaseModel, Field
from datetime import datetime as dt

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