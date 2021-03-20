import os
from config.db_session import Session

session = Session()

sql = """
CREATE SCHEMA IF NOT EXISTS dbbikes
"""
session.execute(sql)

sql = """
CREATE TABLE IF NOT EXISTS stations (
id int NOT NULL AUTO_INCREMENT primary key,
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
    res = session.execute(sql)
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