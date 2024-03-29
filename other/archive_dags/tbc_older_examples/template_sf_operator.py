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
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.contrib.hooks.snowflake_hook import SnowflakeHook
import snowflake.connector

# from airflow.models import Variable

# Set up a specific logger with our desired output level
logging.basicConfig(format="%(message)s")
logger = logging.getLogger("airflow.task")
logger.setLevel(logging.INFO)

SNOWFLAKE_CONN_ID = "snowflake_conn_eg"

SNOWFLAKE_WH = "BIKE_SHOP_DEVELOPER_WH"
SNOWFLAKE_DB = "BIKE_SHOP_NP_RAW_DB"
SNOWFLAKE_SCHEMA = "SALES"
SNOWFLAKE_ROLE = "BIKE_SHOP_NP_DBA"

default_args = {"owner": "airflow", "depends_on_past": False, "email_on_failure": False, "email_on_retry": False, "start_date": days_ago(1), "snowflake_conn_id": SNOWFLAKE_CONN_ID}

conn = snowflake.connector.connect(
    user=os.environ["BIKE_SHOP_DBT_USER"], password=os.environ["BIKE_SHOP_DBT_PASS"], account=os.environ["sf_acc_name_dbt_demo"], warehouse=SNOWFLAKE_WH, database=SNOWFLAKE_DB, schema=SNOWFLAKE_SCHEMA
)


def count1(**context):
    dwh_hook = SnowflakeHook(snowflake_conn_id=SNOWFLAKE_CONN_ID)
    result = dwh_hook.get_first("show tables")
    logging.info(f"result = {result}")


with DAG(dag_id=os.path.basename(__file__).replace(".py", ""), default_args=default_args, schedule_interval=None, tags=["template"]) as dag:

    start_task = DummyOperator(task_id="start", dag=dag)

    end_task = DummyOperator(task_id="end", dag=dag)

    count_query = PythonOperator(task_id="count_query", python_callable=count1)

    # snowflake_query = SnowflakeOperator(
    #    task_id="snowflake_query_eg",
    #    dag=dag,
    #    sql="SELECT current_version()",
    #    snowflake_conn_id=SNOWFLAKE_CONN_ID,
    #    warehouse=SNOWFLAKE_WH,
    #    database=SNOWFLAKE_DB,
    #    schema=SNOWFLAKE_SCHEMA,
    #    role=SNOWFLAKE_ROLE,
    # )

start_task >> count_query >> end_task
