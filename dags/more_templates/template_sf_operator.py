#!/usr/bin/env python3
"""
Python Version  : 3.7
* Name          : template_dag.py
* Description   : Boilerplate Airflow DAG script.
* Created       : 11-06-2021
* Usage         : python3 template_dag.py
"""

__author__ = "Paul Fry"
__version__ = "0.1"

import os
import logging
from time import time
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.contrib.operators.snowflake_operator import SnowflakeOperator
from airflow.contrib.hooks.snowflake_hook import SnowflakeHook

# from airflow.models import Variable

# Set up a specific logger with our desired output level
logging.basicConfig(format="%(message)s")
logger = logging.getLogger("airflow.task")
logger.setLevel(logging.INFO)

SNOWFLAKE_CONN_ID = "test"

SNOWFLAKE_WH = "BIKE_SHOP_DEVELOPER_WH"
SNOWFLAKE_DB = "BIKE_SHOP_NP_RAW_DB"
SNOWFLAKE_SCHEMA = "SALES"
SNOWFLAKE_ROLE = "BIKE_SHOP_NP_DBA"

default_args = {"owner": "airflow", "depends_on_past": False, "email_on_failure": False, "email_on_retry": False, "start_date": days_ago(1), "snowflake_conn_id": SNOWFLAKE_CONN_ID}


def count1(**context):
    dwh_hook = SnowflakeHook(snowflake_conn_id="test")
    result = dwh_hook.get_first("show tables")
    logging.info(f"result = {result}")


with DAG(dag_id=os.path.basename(__file__).replace(".py", ""), default_args=default_args, schedule_interval=None, tags=["template"]) as dag:

    start_task = DummyOperator(task_id="start", dag=dag)

    end_task = DummyOperator(task_id="end", dag=dag)

    count_query = PythonOperator(task_id="count_query", python_callable=count1)

    snowflake_query = SnowflakeOperator(
        task_id="snowflake_query_eg",
        dag=dag,
        sql="show tables",
        warehouse=SNOWFLAKE_WH,
        database=SNOWFLAKE_DB,
        schema=SNOWFLAKE_SCHEMA,
        role=SNOWFLAKE_ROLE,
    )

start_task >> snowflake_query >> end_task
