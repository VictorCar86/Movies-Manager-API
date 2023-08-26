from pydantic import BaseModel, Field

class User(BaseModel):
	email: str = Field(min_length=5, max_length=30)
	password: str = Field(min_length=8)

	model_config = {
		"json_schema_extra": {
			"example": {
				"email": "mail@mail.com",
				"password": "password"
			}
		}
	}