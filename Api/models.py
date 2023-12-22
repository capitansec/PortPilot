import uuid

from sqlalchemy import Column, Integer, String, DateTime, MetaData
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base(metadata=MetaData())


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    uuid = Column(UUID(as_uuid=True), default=str(uuid.uuid4()), unique=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, index=True, nullable=False)
    password = Column(String(64), nullable=False)
    created = Column(DateTime(timezone=True), server_default=func.now())
