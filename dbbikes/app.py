from flask import Flask, render_template, g, jsonify, config
from sqlalchemy import create_engine
from config.db_session import Session
from dbbikes.models.station import Station

APIKEY = "f5c6b9cb5c887092253375f0912332f81099e51d"
NAME = "Dublin"
STATIONS_URI = "https://api.jcdecaux.com/vls/v1/stations"

app = Flask(__name__)

session = Session()

@app.route("/")
def root():
    return app.send_static_file('index.html')


@app.route("/stations")
def stations():
    data = []
    stations = session.query(Station).order_by(Station.id)
    for station in stations:
        data.append(station.to_json())
    return jsonify(stations=data)


@app.route("/stations/<int:station_id>/available")
def get_stations(station_id):
    fetch_station = session.query(Station).get(station_id)
    return jsonify(available_bikes=fetch_station.available_bikes, available_bike_stands=fetch_station.available_bike_stands)


@app.route('/stations/<int:station_id>')
def station(station_id):
    fetch_station = session.query(Station).get(station_id)
    return jsonify(station=fetch_station.to_json())


if __name__ == "__main__":
    app.run(debug=True)
