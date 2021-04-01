import requests
import json
from sqlalchemy import create_engine

APIKEY = "f5c6b9cb5c887092253375f0912332f81099e51d"
NAME = "Dublin"
USER = "ciara"
PASSWORD = "Ciara123"
PORT = "3306"
DB = "dbbikes"
STATIONS_URI = "https://api.jcdecaux.com/vls/v1/stations"
DB_URI = "dbbikes.cvr6gofoxmkp.us-east-2.rds.amazonaws.com"


engine = create_engine(
        "mysql+pymysql://{}:{}@{}:{}/{}".format(
            USER,
            PASSWORD,
            DB_URI,
            PORT,
            DB))
r = requests.get(STATIONS_URI, params={"apiKey": APIKEY, "contract": NAME})


def stations_to_db(text):
    stations = json.loads(text)
    for station in stations:
        vals = (int(station.get('number')), station.get('contract_name'),
                station.get('name'), station.get('address'), station.get('position').get('lat'),
                station.get('position').get('lng'), station.get('banking'), station.get('bonus'),
                int(station.get('bike_stands')), int(station.get('available_bike_stands')),
                int(station.get('available_bikes')),
                station.get('status'), int(station.get('last_update')))
        engine.execute("insert into dbbikes_info "
                       "(number, contract_name, name, address, lat, lng, banking, bonus, bike_stands,"
                       "available_bike_stands, available_bikes, status, last_update)"
                       "values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", vals)

    return


stations_to_db(r.text)
