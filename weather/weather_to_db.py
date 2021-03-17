import os
import datetime
import traceback
import requests
import json
from sqlalchemy import create_engine
from weather_session import Session
from weather import Weather
from weather_api import *

session = Session()


def make_dir(filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)


def make_file_name(now):
    return "data/weather_{}".format(now.strftime("%Y_%m_%d:%H_%M_%S"))


def write_to_file(text, now):
    filename = make_file_name(now)
    make_dir(filename)
    with open(filename, "w") as f:
        f.write(text)


def weather_to_db(text):
    weather = json.loads(text)
    print(type(weather), len(weather))
    weather_instance = Weather(description=weather['weather'][0].get('description'),
                               temp=float(weather['main'].get('temp') - 273.15),
                               last_update=datetime.datetime.fromtimestamp(weather.get('dt')))
    session.add(weather_instance)
    session.commit()
    return


def make_request():
    r = requests.get(URI)
    print(r)
    return r


def execute():
    print("executing")

    try:
        now = datetime.datetime.now()
        r = make_request()
        print(r, now)
        write_to_file(r.text, now)
        weather_to_db(r.text)
    except:
        print(traceback.format_exc())
        if session is None:
            return


execute()
