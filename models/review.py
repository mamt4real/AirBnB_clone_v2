#!/usr/bin/python3
""" Review module for the HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv


class Review(BaseModel, Base):
    """ Review classto store review information """
    __tablename__ = "reviews"
    place_id = Column(
        String(60),
        ForeignKey(
            "places.id",
            ondelete="CASCADE"),
        nullable=False)
    user_id = Column(
        String(60),
        ForeignKey(
            "users.id",
            ondelete="CASCADE"),
        nullable=False)
    text = Column(String(1024),
                  nullable=False)

    if getenv("HBNB_TYPE_STORAGE") == "db":
        user = relationship("User", viewonly=True)
        place = relationship("Place")
    else:
        @property
        def user(self):
            """Review author"""
            from models import storage
            users = storage.all("User")
            key = "User." + self.user_id
            if key in users:
                return users[key]

        @property
        def place(self):
            """place reviewed"""
            from models import storage
            places = storage.all("Place")
            key = "Place." + self.place_id
            if key in places:
                return places[key]
