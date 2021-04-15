from flask import Flask, render_template, jsonify, request
from config.db_session import Session
from dbbikes.models.dublin_bikes_station import DublinBikesStation
import pandas as pd
import numpy as np
import pickle
from sklearn.linear_model import LinearRegression
import time

APIKEY = "f5c6b9cb5c887092253375f0912332f81099e51d"
NAME = "Dublin"
STATIONS_URI = "https://api.jcdecaux.com/vls/v1/stations"

app = Flask(__name__)
app._static_folder = 'web/static'
app.template_folder = 'web/templates'

session = Session()

with open('ml_model/model.pkl', 'rb') as handle:
    model = pickle.load(handle)


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
    SELECT last_update/1000 as updated_on, available_bikes, last_update FROM dbbikes_info
    where number = {station_id}
    """
    df = pd.read_sql_query(sql, session.connection())
    df['last_update'] = pd.to_datetime(df['last_update'], unit='ms')
    result_df = df.set_index('last_update').resample('1d').mean().to_json(orient='values')
    return result_df


@app.route('/predict')
def predict():
    args = request.args
    station_id = int(args.get('station'))
    weekday = int(args.get('weekday'))
    hour = int(args.get('hour'))
    hours = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    hours[hour] = 1
    prediction = model[station_id][weekday].predict([hours])
    result = {'available_bikes': prediction[0][0],
              'temperature': prediction[0][1]}
    return result


if __name__ == "__main__":
    app.run(debug=True)
