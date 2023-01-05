#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import getenv


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(
        String(128), nullable=False
    )

    if getenv("HBNB_TYPE_STORAGE") == "db":
        cities = relationship("City", backref="states")
    else:
        @property
        def cities(self):
            """Getter for cities of the state"""
            from models import storage
            return list(filter(
                lambda c: c.state_id == self.id,
                storage.all("City").values()
            ))
