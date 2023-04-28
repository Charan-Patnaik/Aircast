#%%
import pytest
import re
import pandas as pd
import numpy as np

# TEST CASES
# -----------------------------------------------------------------------------------
# DATA READ
# -----------------------------------------------------------------------------------
#%%
@pytest.fixture
def load_dataset_station_with_params():
    df_station = pd.read_csv('station_with_params.csv')
    return df_station

@pytest.fixture
def load_dataset_station_with_params_list():
    converters = {'parameter name': lambda x: x.strip("[]").replace("'", "").split(", ")}
    df_station = pd.read_csv('station_with_params.csv', converters=converters)
    return df_station


# test to check data type of CountyName column
def test_countyname_type(load_dataset_station_with_params):
    assert load_dataset_station_with_params['CountyName'].dtype == 'object', "CountyName should be a string"

# test to check data type of parameter_name column
def test_parameter_name_type(load_dataset_station_with_params_list):
    assert isinstance(load_dataset_station_with_params_list['parameter name'][0], list), "parameter name should be a list"

# test to check uniqueness of AQSID column
def test_aqsid_unique(load_dataset_station_with_params):
    assert load_dataset_station_with_params['AQSID'].is_unique, "AQSID values are not unique"

#%%
def test_lat_float(load_dataset_station_with_params):
    assert load_dataset_station_with_params['Latitude'].dtype == np.float64, "LAT column should contain floats only"

# %%
def test_lng_float(load_dataset_station_with_params):
    assert load_dataset_station_with_params['Longitude'].dtype == np.float64, "LNG column should contain floats only"

# -----------------------------------------------------------------------------------
# ZIP, LAT, LNG VALIDATION
# -----------------------------------------------------------------------------------

#%%
@pytest.fixture
def load_dataset_zip_with_lat():
    df_zip = pd.read_csv('zip_with_lat.csv')
    return df_zip
# -----------------------------------------------------------------------------------
# data quality checks 
# -----------------------------------------------------------------------------------
#%%
def test_zip_int(load_dataset_zip_with_lat):
    assert load_dataset_zip_with_lat['ZIP'].dtype == np.int64, "ZIP column should contain integers only"

# #%%
def test_lat_float(load_dataset_zip_with_lat):
    assert load_dataset_zip_with_lat['LAT'].dtype == np.float64, "LAT column should contain floats only"

# #%%
def test_lng_float(load_dataset_zip_with_lat):
    assert load_dataset_zip_with_lat['LNG'].dtype == np.float64, "LNG column should contain floats only"


#%%
from fastapi import FastAPI
from fastapi.testclient import TestClient
from .main import app
from routers import user
from routers import service_plans
from routers import admin
import json

client = TestClient(app)

# register user router
app.include_router(user.router)
app.include_router(service_plans.router)
app.include_router(admin.router)

def test_funct():
    response = client.get('/')
    assert response.status_code == 200   

def test_admin_all_users():
    response = client.get("/admin/all-users")
    assert response.status_code == 200
    # print(response.text)
    json_object = json.loads(response.text)
    # print(json_object["users"])
    assert json_object["success"] == True
    assert len(json_object["users"]) == 4


def test_admin_api_sitenames_nearest():
    response = client.get("/admin/api-sitenames-nearest")
    assert response.status_code == 200
    json_object = json.loads(response.text)
    print(json_object)
    # assert json_object["stations"][0]['pollutant'] == ["NO2","CO","PM2.5","PM10","SO2","OZONE"]

