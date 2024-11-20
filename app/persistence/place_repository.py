from app.persistence.repository import SQLAlchemyRepository
from app.models.place import Place
# from app.persistence import db_session

class PlaceRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Place)