from airflow.models import DAG
#from airflow.operators.python_operator import PythonOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from airflow.models.param import Param
from datetime import timedelta


import sys
sys.path.append('/opt/airflow/common_package/')

import data_modeling as de

# %%
dag = DAG(
    dag_id = "model_dag",
    schedule = "0 1 * * 1",   # https://crontab.guru/
    start_date = days_ago(0),
    catchup = False,
    dagrun_timeout = timedelta(minutes=120),
    tags = ["aircast"]
)


with dag:
    build_model = PythonOperator(
        task_id='build_model',
        python_callable= de.generate_mode_for_ma,
        provide_context=True,
        do_xcom_push=True,
        dag=dag,
    )


    build_model