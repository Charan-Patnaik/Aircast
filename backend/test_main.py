#%%
import pytest
import re
import pandas as pd
import numpy as np
from fastapi import FastAPI
from fastapi.testclient import TestClient
from .main import app
from routers import user
from routers import service_plans
from routers import admin
import json

# # TEST CASES
# # -----------------------------------------------------------------------------------
# # DATA QUALITY CHECK ON CSVs
# # -----------------------------------------------------------------------------------

# # -----------------------------------------------------------------------------------
# # 1. STATION DATASET
# # -----------------------------------------------------------------------------------
# #%%
# @pytest.fixture
# def load_dataset_station_with_params():
#     df_station = pd.read_csv('station_with_params.csv')
#     return df_station

# @pytest.fixture
# def load_dataset_station_with_params_list():
#     converters = {'parameter name': lambda x: x.strip("[]").replace("'", "").split(", ")}
#     df_station = pd.read_csv('station_with_params.csv', converters=converters)
#     return df_station


# # test to check data type of CountyName column
# def test_countyname_type(load_dataset_station_with_params):
#     assert load_dataset_station_with_params['CountyName'].dtype == 'object', "CountyName should be a string"

# # test to check data type of parameter_name column
# def test_parameter_name_type(load_dataset_station_with_params_list):
#     assert isinstance(load_dataset_station_with_params_list['parameter name'][0], list), "parameter name should be a list"

# # test to check uniqueness of AQSID column
# def test_aqsid_unique(load_dataset_station_with_params):
#     assert load_dataset_station_with_params['AQSID'].is_unique, "AQSID values are not unique"

# #%%
# def test_lat_float(load_dataset_station_with_params):
#     assert load_dataset_station_with_params['Latitude'].dtype == np.float64, "LAT column should contain floats only"

# # %%
# def test_lng_float(load_dataset_station_with_params):
#     assert load_dataset_station_with_params['Longitude'].dtype == np.float64, "LNG column should contain floats only"


# -----------------------------------------------------------------------------------
# 2.ZIP, LAT, LNG VALIDATION
# -----------------------------------------------------------------------------------

# #%%
# @pytest.fixture
# def load_dataset_zip_with_lat():
#     df_zip = pd.read_csv('zip_with_lat.csv')
#     return df_zip

# #%%
# def test_zip_int(load_dataset_zip_with_lat):
#     assert load_dataset_zip_with_lat['ZIP'].dtype == np.int64, "ZIP column should contain integers only"

# # #%%
# def test_lat_float(load_dataset_zip_with_lat):
#     assert load_dataset_zip_with_lat['LAT'].dtype == np.float64, "LAT column should contain floats only"

# # #%%
# def test_lng_float(load_dataset_zip_with_lat):
#     assert load_dataset_zip_with_lat['LNG'].dtype == np.float64, "LNG column should contain floats only"


#%%

# -----------------------------------------------------------------------------------
# 3. FASTAPI TESTING
# -----------------------------------------------------------------------------------


client = TestClient(app)

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
      yield c

# register user router
app.include_router(user.router)
app.include_router(service_plans.router)
app.include_router(admin.router)

@pytest.fixture(scope="module")
def test_user():
    return {"username": "admin", "password": "spring2023"}

#1
def test_funct(client):
    response = client.get('/')
    assert response.status_code == 200   

#2
def test_login(client, test_user):
  response = client.post("/user/login", data=test_user)
  assert response.status_code == 200
  token = response.json()["access_token"]
  assert token is not None
  return token

#
def test_service_plan(client):
    response = client.get("/service-plan/options")
    assert response.status_code == 200
    print(response.text)
    json_object = json.loads(response.text)
    assert len(json_object) == 3
    assert json_object[0]["id"] == 1
    assert json_object[0]["planName"] == "Free"
    assert json_object[1]["id"] == 2
    assert json_object[1]["planName"] == "Gold"
    assert json_object[2]["id"] == 3
    assert json_object[2]["planName"] == "Platinum"



#3
def test_admin_all_users(client):
    response = client.get("/admin/all-users")
    assert response.status_code == 200
    # print(response.text)
    json_object = json.loads(response.text)
    # print(json_object["users"])
    assert json_object["success"] == True
    # assert len(json_object["users"]) == 4 Testing this  might fail as the users can get created

#4
def test_api_hits_count_user_admin(client, test_user):
    token = test_login(client, test_user)
    response = client.get("/admin/api-hits-count/user/admin?date_request=04%2F26%2F2023", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    json_object = json.loads(response.text)
    assert json_object["success"] == True
    assert len(json_object["api_req"]) == 24


#5
def test_admin_api_hits_previous_days(client, test_user):
    token = test_login(client, test_user)
    response = client.get('/admin/api-hits-previous-days', headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    json_object = json.loads(response.text)
    print(json_object['total_api_hits_in_previous_day'])
    print(json_object['total_successful_api_hits_in_previous_day'])
    print(json_object['total_failed_api_hits_in_previous_day'])

#6
def test_admin_api_hits_compare_success_and_failure(client, test_user):
    token = test_login(client, test_user)
    response = client.get('/admin/all-apis-hits-with-count-compare-success-failure', headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

