import logging
import os
import peewee
import sqlite3
import logging
# ==============================================================

# IMPORTANT - THIS IMPORTS THE DATABASE MODELS LOCATED IN DATABASE_MODELS.PY
from .Data.database_models import *

#=============================================

class Initialize:
    def __init__(self):
        pass

    # TEMPORARY FILES
    def makeLogs(self):
        LOG_FILE = 'providence.log'
        if os.path.isfile(LOG_FILE) and os.access(LOG_FILE, os.R_OK):
            os.remove(LOG_FILE)
        logging.basicConfig(filename='providence.log',
                            level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s'
                            ,datefmt="%H:%M:%S")
        logging.FileHandler('providence.log')
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)

    def makeTemp(self):
        TEMP = "temp"
        if os.path.exists(TEMP) and os.path.isdir(TEMP):
            for filename in os.listdir(TEMP):
                file_path = os.path.join(TEMP, filename)
                os.remove(file_path)
        else:
            try:
                original_umask = os.umask(0)
                os.makedirs('temp', 0o777)  # Use octal notation
            finally:
                os.umask(original_umask)

    # DATABASES
    def makeUser(self):
        db = SqliteDatabase("Data/users.db")
        try:
            db.connect()
        except peewee.OperationalError as e:
            # If the connection is already open, ignore the exception
            if 'Connection already opened' not in str(e):
                logging.error(e)

        db_user = [Profiles,Messages,MessageTopics,UserActivity,UserPreferences]
        db.create_tables([item for item in db_user], safe=True)

    def terminateDatabases(self,db):
        def termination():
            logging.info(f"Initiation of termination procedures. \n")
            db.close()
            logging.info("Termination succeeded.")