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
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
import snowflake.connector

# from airflow.models import Variable

# Set up a specific logger with our desired output level
logging.basicConfig(format="%(message)s")
logger = logging.getLogger("airflow.task")
logger.setLevel(logging.INFO)

default_args = {"owner": "airflow", "depends_on_past": False, "email_on_failure": False, "email_on_retry": False, "start_date": days_ago(1)}

sf_user = os.environ["sf_username_dbt_demo"]
sf_pass = os.environ["sf_pass_dbt_demo"]
sf_account = os.environ["sf_acc_name_dbt_demo"]
# TODO: revert this vars
sf_db = "BIKE_SHOP_NP_RAW_DB"
sf_schema = "utilities"
# sf_db = os.environ["BIKE_SHOP_RAW_DB"]
# sf_schema = os.environ["BIKE_SHOP_SCHEMA"]

# NOTE: I think this initially needs to be commented out. However, it then needs to be uncommented, to successfully run
conn = snowflake.connector.connect(user=sf_user, password=sf_pass, account=sf_account)


def snowf_conn(**kwargs):
    logger.info("Entered function 'snowf_conn'")

    conn = snowflake.connector.connect(user=sf_user, password=sf_pass, account=sf_account)

    cs = conn.cursor()
    try:
        cs.execute("SELECT current_version()")
        one_row = cs.fetchone()
        print(one_row[0])
    finally:
        cs.close()
    conn.close()


with DAG(dag_id=os.path.basename(__file__).replace(".py", ""), default_args=default_args, schedule_interval=None, tags=["template"]) as dag:

    start_task = DummyOperator(task_id="start", dag=dag)

    example_task = PythonOperator(task_id="example_task", python_callable=snowf_conn)

    end_task = DummyOperator(task_id="end", dag=dag)

start_task >> example_task >> end_task
