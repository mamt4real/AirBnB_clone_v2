#!/usr/bin/python3
"""This module defines a class User"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import getenv


class User(BaseModel, Base):
    """This class defines a user by various attributes"""
    __tablename__ = "users"
    email = Column(
        String(128), nullable=False
    )
    password = Column(
        String(128), nullable=False
    )
    first_name = Column(
        String(128), nullable=False
    )
    last_name = Column(
        String(128), nullable=False
    )

    if getenv("HBNB_TYPE_STORAGE") == "db":
        places = relationship("Place")
        reviews = relationship("Review")
    else:
        @property
        def places(self):
            """User places"""
            from models import storage
            return list(filter(
                lambda p: p.user_id == self.id,
                storage.all("Place")
            ))

        @property
        def reviews(self):
            """User reviews"""
            from models import storage
            return list(filter(
                lambda r: r.user_id == self.id,
                storage.all("Review")
            ))
