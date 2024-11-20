""" User model """

from app.persistence import Base
import uuid
import re
from datetime import datetime
from flask_bcrypt import Bcrypt
from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.orm import relationship

bcrypt = Bcrypt()

class User(Base):
    """ User class """
    __tablename__ = 'users'

    # Remember: if you have getters & setters for any of the attributes
    # you can't use the same name for the attributes themselves

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    updated_at = Column(DateTime, nullable=False, default=datetime.now())
    _first_name = Column("first_name", String(50), nullable=False)
    _last_name = Column("last_name", String(50), nullable=False)
    _email = Column("email", String(120), nullable=False, unique=True)
    _password = Column("password", String(128), nullable=False)
    _is_admin = Column("is_admin", Boolean, default=False)
    reviews_r = relationship("Review", back_populates="author_r")
    properties_r = relationship("Place", back_populates="owner_r")

    def __init__(self, first_name, last_name, email, password=None, is_admin = False):
        # NOTE: Attributes that don't already exist will be
        # created when called in the constructor

        if first_name is None or last_name is None or email is None:
            raise ValueError("Required attributes not specified!")

        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.is_admin = is_admin
        self.places = [] # List to store user-owned places
        self.reviews = [] # List to store user-written reviews

        # The method will call the setter
        # self.hash_password(password)
    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        if isinstance(value, str) and 0 < len(value) <= 50:
            self._first_name = value
        else:
            raise ValueError(
                "First name must be a string with a maximum length of 50 characters"
                )

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        if isinstance(value, str) and 0 < len(value) <= 50:
                self._last_name = value
        else:
            raise ValueError(
                "Last name must be a string with a maximum length of 50 characters"
                )

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        """Setter for prop email"""
        # calls the method in the facade object
        from app.services import facade

        # add a simple regex check for email format. Nothing too fancy.
        is_valid_email = len(value.strip()) > 0 and re.search("^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$", value)
        email_exists = facade.get_user_by_email(value.strip())
        if is_valid_email and not email_exists:
            self._email = value
        else:
            if email_exists:
                raise ValueError("Email already exists!")

            raise ValueError("Invalid email format!")

    @property
    def is_admin(self):
        return self._is_admin

    @is_admin.setter
    def is_admin(self, value):
        if isinstance(value, bool):
            self._is_admin = value
        else:
            raise ValueError("is_admin must be a boolean value")