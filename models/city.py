#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv


class City(BaseModel, Base):
    """ The city class, contains state ID and name """
    __tablename__ = "cities"
    state_id = Column(
        String(60),
        ForeignKey(
            "states.id",
            ondelete="CASCADE"),
        nullable=False
    )
    name = Column(String(128), nullable=False)

    if getenv("HBNB_TYPE_STORAGE") == "db":
        state = relationship("State",viewonly=True)
        places = relationship("Place", backref="cities")
    else:
        @property
        def state(self):
            """State the city belongs to"""
            from models import storage
            states = storage.all("State")
            key = "State." + self.state_id
            if key in states:
                return states[key]

        @property
        def places(self):
            """Places in the city"""
            from models import storage
            return list(filter(
                lambda p: p.state_id == self.id,
                storage.all("Place").values()
            ))
