import sqlalchemy as sqla
from sqlalchemy import create_engine
import traceback
import glob
import os
from pprint import pprint
import simplejson as json
import requests
import time
import MySQLdb
from IPython.display import display
import traceback
import datetime
import errno
import pandas as pd
from flaskapp.connect.user_password import *
from weather_api import *
from weather_session import Session

session = Session()

sql = """
CREATE TABLE IF NOT EXISTS weather (
id int NOT NULL AUTO_INCREMENT primary key,
description VARCHAR(256),
temp FLOAT,
last_update DATETIME
)
"""


try:
    res = session.execute(sql)
    print(res.fetchall())
except Exception as e:
    print(e)


def make_dir(filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)


def make_file_name(now):
    return "data/bike_{}".format(now.strftime("%Y_%m_%d:%H_%M_%S"))


def write_to_file(text, now):
    filename = make_file_name(now)
    make_dir(filename)
    with open(filename, "w") as f:
        f.write(text)
