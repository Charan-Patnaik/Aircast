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

# #%%
# ------------------------------------------------------------------------------------
# TEST API
# ------------------------------------------------------------------------------------

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_say_hello():
    response = client.get("/all-users")
    assert response.status_code == 200
    # message = response.json()["message"]
    # assert message == 'Hello World'


# def test_fetch_url():
#     response = client.post(
#         url = "/fetch_url",
#         json = {
#             'year': 2022,
#             'month': 2,
#             'date': 6,
#             'station': 'Pytest2'
#             }
#         )
#     assert response.status_code == 200
#     message = response.json()["url"]
#     assert message == 'https://noaa-nexrad-level2.s3.amazonaws.com/index.html#2022/02/06/Pytest2'
    



# %%
# ---------------- TEST FAST API --------------------
