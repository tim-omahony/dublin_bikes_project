from flask import Flask, render_template, g, jsonify, config
import json
from jinja2 import Template
from sqlalchemy import create_engine
import requests
import pandas as pd

APIKEY = "f5c6b9cb5c887092253375f0912332f81099e51d"
NAME = "Dublin"
USER = "ciara"
PASSWORD = "Ciara123"
PORT = "3306"
DB = "dbbikes"
STATIONS_URI = "https://api.jcdecaux.com/vls/v1/stations"
URI = "dbbikes.cvr6gofoxmkp.us-east-2.rds.amazonaws.com"

app = Flask(__name__)


@app.route("/")
def root():
    return app.send_static_file('index.html')


def connect_to_database():
    engine = create_engine(
        "mysql+pymysql://{}:{}@{}:{}/{}".format(
            USER,
            PASSWORD,
            URI,
            PORT,
            DB,
            echo=True))
    return engine


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
    return db


@app.route("/stations")
def stations():
    engine = get_db()
    data = []
    rows = engine.execute("""SELECT s1.*
                             FROM dbbikes_info s1
                             WHERE s1.id = (SELECT s2.id
                                            FROM dbbikes_info s2
                                            WHERE s2.number = s1.number
                                            ORDER BY s2.id DESC
                                            LIMIT 1)
                             GROUP BY s1.number;""")
    for row in rows:
        data.append(dict(row))
    return jsonify(stations=data)


@app.route("/available/<int:station_id>")
def get_stations(station_id):
    engine = get_db()
    data = []
    rows = engine.execute("""SELECT available_bikes 
                             FROM dbbikes_info
                             WHERE number = {};""".format(station_id))
    for row in rows:
        data.append(dict(row))

    return jsonify(available=data)


@app.route('/station/<int:station_id>')
def station(station_id):
    return 'Retrieving info for Station: {}'.format(station_id)


if __name__ == "__main__":
    app.run(debug=True)
