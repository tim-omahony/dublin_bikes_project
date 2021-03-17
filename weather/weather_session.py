from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import connectors
import pymysql

USER = "root"
PASSWORD = "Ylu3shin123!"
URI = "127.0.0.1"
PORT = "3306"
DB = "dbbikes"
engine = create_engine("mysql+pymysql://{}:{}@{}:{}/{}".format(USER, PASSWORD, URI, PORT, DB), echo=True)

# create a configured "Session" class
Session = sessionmaker(bind=engine)

