#%%
import pymysql
import os
from dotenv import load_dotenv
import pytest

#%%
load_dotenv()

#%%
# Load the environment variables
DB_HOST = os.environ.get('DB_HOST')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_NAME = os.environ.get('DB_NAME')
DB_PORT = 3306

#%%
def create_conn():
    # Connect to the database
    conn = pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    print("connected")
    return conn


@pytest.fixture()
def cursor():
    # Establish a connection and return a cursor object
    conn = create_conn()
    cursor = conn.cursor()
    yield cursor
    conn.close()

#%%
#1
# Define a function to test the SQL data
def test_sql_data(cursor):
    cursor.execute("SELECT * FROM Stations LIMIT 10;")
    result = cursor.fetchall()
    return result

#2
def test_station_id(cursor):
    # Test that all station ids are unique and greater than 0
    cursor.execute("SELECT id FROM Stations")
    ids = cursor.fetchall()
    assert len(ids) == len(set(ids))  # all ids are unique
    assert all(id[0] > 0 for id in ids)  # all ids are greater than 0

#3
def test_station_location(cursor):
    # Test that all station locations are within valid coordinates
    cursor.execute("SELECT latitude, longitude FROM Stations")
    locations = cursor.fetchall()
    assert all(-90 <= location[0] <= 90 and -180 <= location[1] <= 180 for location in locations)
