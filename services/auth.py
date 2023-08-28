from db.config import Session
from schemas.user import User
from models.user import User as UserModel
from utils.jwt_manager import create_token

class AuthService:
    def __init__(self) -> None:
        self.db = Session()

    def signup_user(self, user: User) -> bool:
        user_exist = self.db.query(UserModel).filter_by(email= user.email).one_or_none()
        if user_exist:
            return False
        self.db.add( UserModel(**dict(user)) )
        self.db.commit()
        return True

    def login_user(self, user: User) -> str | bool:
        user_exist = self.db.query(UserModel).\
            filter_by(email= user.email, password= user.password).first()
        if not user_exist:
            return False
        return create_token({'email': user.email})