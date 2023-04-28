#%%
from airflow.models import DAG
#from airflow.operators.python_operator import PythonOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from airflow.models.param import Param
from datetime import timedelta

import sys
sys.path.append('/opt/airflow/common_package/')

import data_extraction as de


dag = DAG(
    dag_id = "cache_clear_dag",
    schedule = "0 1 * * *",   # https://crontab.guru/
    start_date = days_ago(0),
    catchup = False,
    dagrun_timeout = timedelta(minutes=60),
    tags = ["aircast"]
)

with dag:

    cache_clear = PythonOperator(
        task_id='cache_clear',
        python_callable= de.clear_cache,
        provide_context=True,
        do_xcom_push=True,
        dag=dag,
    )


    cache_clear