# Aircast

### Overview about our Application
This is a complete system ensuring user to get access to Air Quality Prediction. It helps to provide advance warning to our application users about potential air quality problems. This allows people to take precautions to protect their health, such as staying indoors or wearing masks. It also enables policymakers to take action to mitigate the effects of poor air quality, such as implementing restrictions on certain activities that contribute to air pollution. 



### Live Application Links:

**CodeLabs & Reports:** https://codelabs-preview.appspot.com/?file_id=16Ka_g7q11hxCaiDtUhf8-CdDosMPoCXQ0UdtEbx7SA0#1

**Airflow:** http://ec2-44-202-229-216.compute-1.amazonaws.com:8080/

**Streamlit:** http://ec2-54-83-127-235.compute-1.amazonaws.com/

**FastAPI:** http://ec2-54-83-127-235.compute-1.amazonaws.com:8000/docs

**MaaS Hosted URL:** http://3.93.199.166/docs



### Arch Diagram

<img src = 'https://github.com/BigDataIA-Spring2023-Team-05/Aircast/blob/main/ArchDiag.png' />




### Installation:
1. Clone the repository (https://github.com/BigDataIA-Spring2023-Team-05/Aircast.git)

2. Create the .env file inside the main folder. Follow the Aircast Github repository to sample_env.env file for the complete list of variables that need to be added in it.

3. Install the packages listed in requirements.txt 




### Pre-requisites to execute this project

1.Amazon Web Services account

2.Docker Desktop Application

3.AWS access and secret keys

4.OpenAI (Chat GPT) API key



### CLI:
There is a CLI (Command-Line-Interface) in order to provide user the access to the data via AWS S3 bucket.

Commands to access them:
my-cli-app --help

Example download file function: my-cli-app downloadfile -s 100031007 --from 2022-11-01 --to 2022-11-15

This will generate the downloadable link: https://github.com/BigDataIA-Spring2023-Team-05/Aircast.git


### Project Directory Tree:

```
📦 
├─ .github
│  └─ workflows
│     └─ main.yml
├─ .gitignore
├─ ArchDiag.png
├─ README.md
├─ airflow
│  ├─ .gitignore
│  ├─ Dockerfile
│  ├─ common_package
│  │  ├─ ARIMA.py
│  │  ├─ LSTM.py
│  │  ├─ __init__.py
│  │  ├─ data
│  │  │  └─ combine_data.csv
│  │  ├─ data_extraction.py
│  │  ├─ data_modeling.py
│  │  ├─ database
│  │  │  └─ connection.py
│  │  └─ generate_pickle_files.py
│  ├─ dags
│  │  ├─ cache_day.py
│  │  ├─ data_dags.py
│  │  └─ model_dag.py
│  └─ docker-compose.yaml
├─ backend
│  ├─ Dockerfile
│  ├─ __init__.py
│  ├─ aws_cloud
│  │  ├─ __init__.py
│  │  ├─ cloud_watch.py
│  │  └─ s3_upload.py
│  ├─ config
│  │  └─ db.py
│  ├─ main.py
│  ├─ middlewares
│  │  ├─ __init__.py
│  │  ├─ oauth2.py
│  │  └─ requests_logs.py
│  ├─ models
│  │  ├─ Request_Logs.py
│  │  ├─ Service_Plan.py
│  │  ├─ Stations.py
│  │  ├─ StationsData.py
│  │  ├─ StationsDataDaily.py
│  │  ├─ User.py
│  │  ├─ ZipDataDailyCache.py
│  │  ├─ Zipcode.py
│  │  └─ __init__.py
│  ├─ repository
│  │  ├─ __init__.py
│  │  ├─ requests_logs.py
│  │  ├─ service_plans.py
│  │  ├─ stations.py
│  │  ├─ user.py
│  │  └─ zipcode.py
│  ├─ requirements.txt
│  ├─ routers
│  │  ├─ admin.py
│  │  ├─ aircast.py
│  │  ├─ service_plans.py
│  │  └─ user.py
│  ├─ schemas
│  │  ├─ Responses.py
│  │  ├─ Service_Plan.py
│  │  ├─ User.py
│  │  ├─ __init__.py
│  │  └─ dashboard.py
│  ├─ setup.py
│  ├─ station_with_params.csv
│  ├─ utils
│  │  ├─ JWT_token.py
│  │  ├─ __init__.py
│  │  ├─ hashing.py
│  │  └─ redis.py
│  ├─ zip_code_with_state_coor.csv
│  ├─ zip_code_with_state_coordinates.csv
│  └─ zip_with_lat.csv
├─ build
│  └─ lib
│     ├─ backend
│     │  ├─ __init__.py
│     │  ├─ aws_cloud
│     │  │  ├─ __init__.py
│     │  │  ├─ cloud_watch.py
│     │  │  └─ s3_upload.py
│     │  ├─ main.py
│     │  ├─ middlewares
│     │  │  ├─ __init__.py
│     │  │  ├─ oauth2.py
│     │  │  └─ requests_logs.py
│     │  ├─ models
│     │  │  ├─ Request_Logs.py
│     │  │  ├─ Service_Plan.py
│     │  │  ├─ Stations.py
│     │  │  ├─ StationsData.py
│     │  │  ├─ StationsDataDaily.py
│     │  │  ├─ User.py
│     │  │  ├─ ZipDataDailyCache.py
│     │  │  ├─ Zipcode.py
│     │  │  └─ __init__.py
│     │  ├─ repository
│     │  │  ├─ __init__.py
│     │  │  ├─ requests_logs.py
│     │  │  ├─ service_plans.py
│     │  │  ├─ stations.py
│     │  │  ├─ user.py
│     │  │  └─ zipcode.py
│     │  ├─ schemas
│     │  │  ├─ Responses.py
│     │  │  ├─ Service_Plan.py
│     │  │  ├─ User.py
│     │  │  ├─ __init__.py
│     │  │  └─ dashboard.py
│     │  ├─ setup.py
│     │  ├─ test_db.py
│     │  ├─ test_main.py
│     │  └─ utils
│     │     ├─ JWT_token.py
│     │     ├─ __init__.py
│     │     ├─ hashing.py
│     │     └─ redis.py
│     └─ maas
│        ├─ __init__.py
│        ├─ main.py
│        └─ s3_model.py
├─ cli
│  ├─ config
│  └─ main.py
├─ config
├─ dist
│  ├─ my_cli_app-0.1.0-py3-none-any.whl
│  └─ my_cli_app-0.1.0.tar.gz
├─ docker-compose.yml
├─ frontend
│  ├─ Dockerfile
│  ├─ login.py
│  ├─ pages
│  │  ├─ 01_Home.py
│  │  ├─ 02_Register.py
│  │  └─ 04_Analytics.py
│  └─ requirements.txt
├─ maas
│  ├─ .gitignore
│  ├─ __init__.py
│  ├─ main.py
│  ├─ requirements.txt
│  └─ s3_model.py
├─ ml
│  ├─ .gitignore
│  ├─ LSTM.ipynb
│  ├─ ML model for air quality prediction.ipynb
│  ├─ ML_test.ipynb
│  ├─ aqi_calculation.py
│  ├─ data_extraction.ipynb
│  ├─ generate_pickle_files.py
│  ├─ lstm_air_quality.ipynb
│  ├─ lstm_new.py
│  ├─ prediction_pickle.py
│  └─ s3_ma_filter.ipynb
├─ my_cli_app.egg-info
│  ├─ PKG-INFO
│  ├─ SOURCES.txt
│  ├─ dependency_links.txt
│  ├─ entry_points.txt
│  ├─ requires.txt
│  └─ top_level.txt
├─ nginx
│  ├─ Dockerfile
│  └─ project.conf
├─ scripts
│  └─ aircast.sql
├─ setup.py
├─ station_with_params.csv
├─ test
│  ├─ test_db.py
│  └─ test_main.py
└─ zip_code_with_state_coordinates.csv
```
©generated by [Project Tree Generator](https://woochanleee.github.io/project-tree-generator)



## Team Information and Contribution 

Name | Contribution 
--- | --- |
Rishabh Jain | 25% 
Venkata Sai Charan Amiti | 25% 
Varsha Hindupur | 25% 
Krishica Gopalakrishnan | 25% 



### Attestation:
WE ATTEST THAT WE HAVEN’T USED ANY OTHER STUDENTS’ WORK IN OUR ASSIGNMENT AND ABIDE BY THE POLICIES LISTED IN THE STUDENT HANDBOOK.



