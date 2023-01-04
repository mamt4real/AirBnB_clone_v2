#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""

import os

storagetype = os.environ.get("HBNB_TYPE_STORAGE")
storage = None

match storagetype:
    case "db":
        from models.engine.db_storage import DBStorage
        storage = DBStorage()
    case _:
        from models.engine.file_storage import FileStorage
        storage = FileStorage()

if storage is not None:
    storage.reload()
