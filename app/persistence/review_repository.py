from app.models.review import Review
from app.persistence.repository import SQLAlchemyRepository
# from app.persistence import db_session

class ReviewRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Review)

    # def get_reviews_by_place(self, place_id):
    #

    # def get_reviews_by_user(self, user_id):
    #