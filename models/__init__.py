#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""
from models.engine.file_storage import FileStorage
from models.engine.db_storage import DBStorage
import os


storagetype = os.environ.get("HBNB_TYPE_STORAGE")
storage = None


match storagetype:
    case "file":
        storage = FileStorage()
    case "db":
        storage = DBStorage()
    case _ :
        raise ValueError("Storage type is not defined!!")


if storage is not None:
    storage.reload()
