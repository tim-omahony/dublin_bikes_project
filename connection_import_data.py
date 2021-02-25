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
from user_password import *
from api_details import *

URI = "dbbikes.cjlp5umzs5hs.us-east-1.rds.amazonaws.com"
PORT = "3306"
DB = "dbbikes"
engine = create_engine("mysql+mysqldb://{}:{}@{}:{}/{}".format(USER, PASSWORD, URI, PORT, DB), echo=True)

sql = """
CREATE SCHEMA IF NOT EXISTS dbbikes
"""
engine.execute(sql)

for res in engine.execute("SHOW VARIABLES;"):
    print(res)

sql = """
CREATE TABLE IF NOT EXISTS station (
address VARCHAR(256),
banking INTEGER,
bike_stands INTEGER,
bonus INTEGER,
contract_name VARCHAR(256),
name VARCHAR(256),
number INTEGER,
position_lat REAL,
position_lng REAL,
status VARCHAR(256),
available_bikes INTEGER,
available_bike_stands INTEGER,
last_update DATETIME
)
"""
try:
    res = engine.execute("DROP TABLE IF EXISTS station")
    res = engine.execute(sql)
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


def stations_to_db(text):
    stations = json.loads(text)
    print(type(stations), len(stations))
    for station in stations:
        print(station)
        vals = (station.get('address'), int(station.get('banking')), station.get('bike_stands'),
                int(station.get('bonus')), station.get('contract_name'), station.get('name'),
                station.get('number'), station.get('position').get('lat'), station.get('position').get('lng'),
                station.get('status'), int(station.get('available_bikes')), int(station.get('available_bike_stands')),
                int(station.get('last_update'))
                )
        engine.execute("insert into station values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", vals)
    return

# Select
#     FROM_UNIXTIME({timestampcolumn here}) asDateTime_Column
# FROM
#     {tablenamehere}
def make_request():
    r = requests.get(STATIONS, params={"apiKey": APIKEY, "contract": NAME})
    print(r)
    return r


def execute():
    print("executing")

    try:
        now = datetime.datetime.now()
        r = make_request()
        print(r, now)
        write_to_file(r.text, now)
        stations_to_db(r.text)
        time.sleep(5*60)
    except:
        print(traceback.format_exc())
        if engine is None:
            return


execute()

