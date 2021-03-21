import os
import simplejson as json
import requests
import time
import traceback
import datetime
from dbbikes.models.dublin_bikes_station import DublinBikesStation
from config.db_session import Session
NAME = "Dublin"
STATIONS = "https://api.jcdecaux.com/vls/v1/stations"
APIKEY = "d337450524e824d9d4323afbebd4ed51f242c995"


session = Session()


def stations_to_db(text):
    stations = json.loads(text)
    print(type(stations), len(stations))
    for station in stations:
        existing_station = session.query(DublinBikesStation).filter_by(address=station.get('address')).first()
        if existing_station is not None:
            session.query(DublinBikesStation).filter_by(id=existing_station.id).update(dict(status=station.get('status'),
                                                                                    available_bikes=int(station.get('available_bikes')),
                                                                                    available_bike_stands=int(station.get('available_bike_stands')),
                                                                                    last_update=datetime.datetime.fromtimestamp(station.get('last_update') / 1e3)))
            session.commit()
        else:
            print(station)
            station_instance = DublinBikesStation(address=station.get('address'), banking=int(station.get('banking')), bike_stands=station.get('bike_stands'),
                    bonus=int(station.get('bonus')), contract_name=station.get('contract_name'), name=station.get('name'),
                    number=station.get('number'), lat=station.get('position').get('lat'), lng=station.get('position').get('lng'),
                    status=station.get('status'), available_bikes=int(station.get('available_bikes')), available_bike_stands=int(station.get('available_bike_stands')),
                    last_update=datetime.datetime.fromtimestamp(station.get('last_update') / 1e3)
                    )
            session.add(station_instance)
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
        stations_to_db(r.text)
    except:
        print(traceback.format_exc())
        if session is None:
            return


execute()
