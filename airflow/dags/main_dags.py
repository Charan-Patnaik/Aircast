#%%
import airflow
from airflow.models import DAG
#from airflow.operators.python_operator import PythonOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from airflow.models.param import Param
from datetime import timedelta
import pandas as pd
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split
import os
import urllib.request
from datetime import datetime
from airflow.models import data_extraction as de
from airflow.models import ARIMA as arima_model

#%%
# my_arima = ARIMA()

import sys
sys.path.append('/opt/airflow/models/')

# %%
dag = DAG(
    dag_id = "modelservice",
    schedule = "0 0 * * *",   # https://crontab.guru/
    start_date = days_ago(0),
    catchup = False,
    dagrun_timeout = timedelta(minutes=60),
    tags = ["damg7245"]
)

with dag:

    air_data_extraction_daily = PythonOperator(
        task_id='air_data_extraction_daily',
        python_callable= de.data_extraction_daily,
        provide_context=True,
        do_xcom_push=True,
        dag=dag,
    )

    arima_data_modeling = PythonOperator(
        task_id='arima_data_modeling',
        python_callable= arima_model.arima_execution,
        provide_context=True,
        do_xcom_push=True,
        dag=dag,
    )

    # Flow
    air_data_extraction_daily >> arima_data_modeling

