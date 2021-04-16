from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
environment = os.environ.get('FLASK_ENV') or 'development'
if environment == 'development':
    from config.db_details import *
else:
    from config.db_details_prod import *

engine = create_engine("mysql+pymysql://{}:{}@{}:{}/{}".format(USER, PASSWORD, URI, PORT, DB), pool_recycle=3600, echo=True)

# create a configured "Session" class
Session = sessionmaker(bind=engine)

