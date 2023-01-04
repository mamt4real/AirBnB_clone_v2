#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.city import City


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(
        String(128), nullable=False
    )

    cities = relationship("City")

    @property
    def cities(self):
        """Getter for cities of the state"""
        from models import storage
        return list(filter(
            lambda c: c.state_id == self.id,
            storage.all(City)
        ))
