from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import connectors
from db_details import *

engine = create_engine("mysql+pymysql://{}:{}@{}:{}/{}".format(USER, PASSWORD, URI, PORT, DB), echo=True)

# create a configured "Session" class
Session = sessionmaker(bind=engine)

