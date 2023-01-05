#!/usr/bin/python3
"""This File set up the engine to handle"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

# Useful Environment variables
hbnbenv = os.environ.get("HBNB_ENV")
sqluser = os.environ.get("HBNB_MYSQL_USER")
sqlpwd = os.environ.get("HBNB_MYSQL_PWD")
sqlhost = os.environ.get("HBNB_MYSQL_HOST")
sqldb = os.environ.get("HBNB_MYSQL_DB")


class DBStorage:
    """Database Storage Class"""
    __engine = None
    __session = None

    def __init__(self):
        """Initializes the engine and session"""
        DBStorage.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(
                sqluser, sqlpwd, sqlhost, sqldb),
            pool_pre_ping=True)
        if hbnbenv == 'test':
            Base.metadata.drop_all(
                DBStorage.__engine)

    def all(self, cls=None):
        """Retrieve all instances in the db"""
        db = DBStorage.__session
        result = {}
        classes = (
            State, City, User, Place,
            Amenity, Review)
        if cls is not None:
            classes = (cls,)
        for cls in classes:
            docs = db.query(cls).all()
            for doc in docs:
                key = "{}.{}".format(
                    cls.__name__,
                    doc.id)
                result[key] = doc
        return result

    def new(self, obj):
        """Stores a new object in the database"""
        db = DBStorage.__session
        db.add(obj)

    def save(self):
        """persist all changes in the database"""
        DBStorage.__session.commit()

    def delete(self, obj):
        """delete an object in the database"""
        db = DBStorage.__session
        cls = obj.__class__
        db.query(cls).where(
            cls.id == obj.id
        ).delete()
        self.save()

    def reload(self):
        """Create and set up the session"""
        Base.metadata.create_all(
            DBStorage.__engine)
        maker = sessionmaker(
            bind=DBStorage.__engine,
            autocommit=False,
            expire_on_commit=False,
            autoflush=False)
        DBStorage.__session = scoped_session(maker)
