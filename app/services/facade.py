from app.persistence.repository import SQLAlchemyRepository
from app.persistence.user_repository import UserRepository
from app.persistence.review_repository import ReviewRepository
from app.persistence.place_repository import PlaceRepository
from app.persistence.amenity_repository import AmenityRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from app.persistence import db_session

class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.review_repo = ReviewRepository()
        self.place_repo = PlaceRepository()
        self.amenity_repo = AmenityRepository()
        # self.amenity_repo = SQLAlchemyRepository(Amenity)
    # In case anyone is curious about the **
    # https://www.geeksforgeeks.org/what-does-the-double-star-operator-mean-in-python/

    # --- Users ---
    def create_user(self, user_data):
        user = User(**user_data)
        user.hash_password(user_data['password'])
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_user_by_email(email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        self.user_repo.update(user_id, user_data)

    # def delete_user(self, user_id):
    #     self.review_repo.delete(user_id)

    def delete_user(self, user_id):
        user = db_session.query(User).get(user_id)
        if not user:
            raise ValueError("User not found")
        db_session.delete(user)
        db_session.commit()

    # --- User Relationship methods ---
    def get_user_places(self, user_id):
        user = self.user_repo.get(user_id)
        if not user:
            return None
        return user.properties_r
    def get_user_reviews(self, user_id):
        user = self.user_repo.get(user_id)
        if not user:
            return None
        return user.reviews_r

    #--- Amenities ---
    #sed during record insertion to prevent duplicate amenities
    def get_amenity_by_name(self, name):
        return self.amenity_repo.get_by_attribute('name', name)

    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        self.amenity_repo.update(amenity_id, amenity_data)

    def delete_amenity(self, amenity_id):
        self.amenity_repo.delete(amenity_id)

    # --- Amenity Relationship methods ---
    def get_amenity_places(self, amenity_id):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        return amenity.places_r

    # --- Places ---
    def create_place(self, place_data):
        place = Place(**place_data)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        self.place_repo.update(place_id, place_data)
    
    def delete_place(self, place_id):
        place = db_session.query(Place).get(place_id)
        if not place:
            raise ValueError("Place not found")
        db_session.delete(place)
        db_session.commit()


    def delete_place(self, place_id):
        self.place_repo.delete(place_id)

    # --- Place Relationship methods ---
    def get_place_amenities(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            return None
        return place.amenities_r

    def get_place_reviews(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            return None
        return place.reviews_r

    def get_place_owner(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            return None
        return place.owner_r

    # --- Reviews ---
    def create_review(self, review_data):
        review = Review(**review_data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        return self.review_repo.get_by_attribute('place_id', place_id)

    def update_review(self, review_id, review_data):
        self.review_repo.update(review_id, review_data)

    # def delete_review(self, review_id):
    #     self.review_repo.delete(review_id)
    def delete_review(self, review_id):
        review = db_session.query(Review).get(review_id)
        if not review:
            raise ValueError("Review not found")
        db_session.delete(review)
        db_session.commit()

    # --- Review Relationship methods ---
    def get_review_author(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            return None
        return review.author_r

    def get_review_place(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            return None
        return review.place_r