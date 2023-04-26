#%%
from airflow.models import DAG
#from airflow.operators.python_operator import PythonOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from airflow.models.param import Param
from datetime import timedelta

#%%
# my_arima = ARIMA()

import sys
sys.path.append('/opt/airflow/common_package/')

import data_extraction as de

# %%
dag = DAG(
    dag_id = "daily_data_collection",
    schedule = "20 1 * * *",   # https://crontab.guru/
    start_date = days_ago(0),
    catchup = False,
    dagrun_timeout = timedelta(minutes=60),
    tags = ["aircast"]
)

with dag:

    air_data_extraction_daily = PythonOperator(
        task_id='air_data_extraction_daily',
        python_callable= de.data_extraction_daily,
        provide_context=True,
        do_xcom_push=True,
        dag=dag,
    )

        
    air_data_extraction_two_daily = PythonOperator(
        task_id='air_data_extraction_two_daily',
        python_callable= de.data_extraction_two_days,

        provide_context=True,
        do_xcom_push=True,
        dag=dag,
    )


    # Flow
    # air_data_extraction_daily >> lstm_data_modeling



    # arima_data_modeling = PythonOperator(
    #     task_id='arima_data_modeling',
    #     python_callable= arima_model.arima_execution,
    #     provide_context=True,
    #     do_xcom_push=True,
    #     dag=dag,
    # )

    # Flow
    air_data_extraction_daily >> air_data_extraction_two_daily


