#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer, Float, Table
from sqlalchemy.orm import relationship
from os import getenv


place_amenity = Table(
    "place_amenity", Base.metadata,
    Column(
        "place_id", String(60),
        ForeignKey("places.id"),
        primary_key=True,
        nullable=False),
    Column(
        "amenity_id", String(60),
        ForeignKey("amenities.id"),
        primary_key=True,
        nullable=False)
)


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"
    city_id = Column(
        String(60),
        ForeignKey(
            "cities.id",
            ondelete="CASCADE"
        ),
        nullable=False)
    user_id = Column(
        String(60),
        ForeignKey(
            "users.id",
            ondelete="CASCADE"
        ),
        nullable=False)
    name = Column(
        String(128), nullable=False
    )
    description = Column(
        String(1024), nullable=False
    )
    number_rooms = Column(
        Integer, nullable=False,
        default=0, server_default="0"
    )
    number_bathrooms = Column(
        Integer, nullable=False,
        default=0, server_default="0"
    )
    max_guest = Column(
        Integer, nullable=False,
        default=0, server_default="0"
    )
    price_by_night = Column(
        Integer, nullable=False,
        default=0, server_default="0"
    )
    latitude = Column(Float)
    longitude = Column(Float)
    amenity_ids = []

    if getenv("HBNB_TYPE_STORAGE") == "db":
        user = relationship("User")
        city = relationship("City")
        reviews = relationship("Review")
    else:
        @property
        def reviews(self):
            """reviews associated with the place"""
            from models import storage
            return list(filter(
                lambda r: r.place_id == self.id,
                storage.all("Review").values()
            ))

        @property
        def user(self):
            """user associated with this place (owner)"""
            from models import storage
            users = storage.all("User")
            key = "User." + self.user_id
            if key in users:
                return users[key]

        @property
        def city(self):
            """city associated with this place"""
            from models import storage
            cities = storage.all("City")
            key = "City." + self.user_id
            if key in cities:
                return cities[key]
