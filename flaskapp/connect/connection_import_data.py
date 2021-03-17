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
from flaskapp.station import Station
from user_password import *
from api_details import *
from db_session import Session

session = Session()


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
        stationInstance = Station(address=station.get('address'), banking=int(station.get('banking')), bike_stands=station.get('bike_stands'),
                bonus=int(station.get('bonus')), contract_name=station.get('contract_name'), name=station.get('name'),
                number=station.get('number'), position_lat=station.get('position').get('lat'), position_lng=station.get('position').get('lng'),
               status=station.get('status'), available_bikes=int(station.get('available_bikes')), available_bike_stands=int(station.get('available_bike_stands')),
                last_update=datetime.datetime.fromtimestamp(station.get('last_update') / 1e3)
                )
        session.add(stationInstance)
        session.commit()
    return


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
        if session is None:
            return


execute()
