from app import db
import uuid
from datetime import datetime, timezone
from app.persistence import Base
from sqlalchemy import Column, String, DateTime

class BaseModel(Base):
    __abstract__ = True  # This ensures SQLAlchemy does not create a table for BaseModel

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))