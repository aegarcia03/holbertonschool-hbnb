from app.models.amenity import Amenity
from app.persistence.repository import SQLAlchemyRepository

class AmenityRepository(SQLAlchemyRepository):
    """Amenity repository class"""
    def __init__(self):
        super().__init__(Amenity)