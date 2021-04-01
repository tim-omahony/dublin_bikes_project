from flask import Flask, render_template, g, jsonify, config
from sqlalchemy import create_engine
from config.db_session import Session
from dbbikes.models.dublin_bikes_station import DublinBikesStation, DublinBikesStationHistory
import pandas as pd

APIKEY = "f5c6b9cb5c887092253375f0912332f81099e51d"
NAME = "Dublin"
STATIONS_URI = "https://api.jcdecaux.com/vls/v1/stations"

app = Flask(__name__)
app._static_folder = 'web/static'
app.template_folder = 'web/templates'

session = Session()


@app.route("/")
def root():
    return render_template('index.html')


@app.route("/stations")
def stations():
    data = []
    stations = session.query(DublinBikesStation).order_by(DublinBikesStation.id)
    for station in stations:
        data.append(station.to_json())
    return jsonify(stations=data)


@app.route("/stations/<int:station_id>/available")
def get_stations(station_id):
    fetch_station = session.query(DublinBikesStation).get(station_id)
    return jsonify(available_bikes=fetch_station.available_bikes,
                   available_bike_stands=fetch_station.available_bike_stands)


@app.route('/stations/<int:station_id>')
def station(station_id):
    fetch_station = session.query(DublinBikesStation).get(station_id)
    return jsonify(station=fetch_station.to_json())


@app.route('/stations/occupancy/<int:station_id>')
def get_occupancy(station_id):
    sql = f"""
    SELECT last_update/1000 as updated_on, available_bikes, available_bike_stands, last_update FROM dbbikes_info
    where number = {station_id}
    """
    df = pd.read_sql_query(sql, session.connection())
    df['last_update'] = pd.to_datetime(df['last_update'], unit='ms')
    result_df = df.set_index('last_update').resample('1d').mean().to_json(orient='values')
    return result_df


if __name__ == "__main__":
    app.run(debug=True)