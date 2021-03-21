import os
from config.db_session import Session

session = Session()

sql = """
CREATE SCHEMA IF NOT EXISTS dbbikes
"""
session.execute(sql)

sql = """
CREATE TABLE IF NOT EXISTS dublin_bikes_stations (
id int NOT NULL AUTO_INCREMENT primary key,
address VARCHAR(256),
banking INTEGER,
bike_stands INTEGER,
bonus INTEGER,
contract_name VARCHAR(256),
name VARCHAR(256),
number INTEGER,
lat REAL,
lng REAL,
status VARCHAR(256),
available_bikes INTEGER,
available_bike_stands INTEGER,
last_update DATETIME
)
"""
try:
    res = session.execute(sql)
    print(res.fetchall())
except Exception as e:
    print(e)



