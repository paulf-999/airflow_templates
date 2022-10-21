#!/usr/bin/env python3
"""
Python Version  : 3.10
* Name          : read_ip_from_dag_conf.py
* Description   : Read input from the DAG conf
* Created       : 28-09-2022
"""

__author__ = "Paul Fry"
__version__ = "0.1"

import os
import logging
import pendulum
import importlib
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.operators.python import get_current_context

# Set up a specific logger with our desired output level
logging.basicConfig(format="%(message)s")
logger = logging.getLogger("airflow.task")
logger.setLevel(logging.INFO)

local_tz = pendulum.timezone("Australia/Melbourne")
dag_path = os.path.dirname(os.path.abspath(__file__))
dag_name = os.path.basename(dag_path)
dag_root = os.path.dirname(dag_path)


def get_ips():
    context = get_current_context()
    # payload was the input passed into this Airflow DAG
    payload = context["dag_run"].conf
    division = payload["division"]
    src_tbl = payload["src_tbl"]

    logger.info(f"payload = {payload}")
    logger.info(f"division = {division}")
    logger.info(f"src_tbl = {src_tbl}")

    return payload, division, src_tbl


helpers = importlib.import_module(".__dag_helpers", package=dag_name)
queries = importlib.import_module(".__sql_queries", package=dag_name)

default_args = {"owner": "airflow", "depends_on_past": False, "email_on_failure": False, "email_on_retry": False, "start_date": pendulum.now(local_tz).subtract(days=1)}
doc_md = helpers.try_render_readme(dag_path)

with DAG(dag_id=dag_name, doc_md=doc_md, default_args=default_args, schedule_interval=None, tags=["example"]) as dag:

    # Create tasks
    start_task = DummyOperator(task_id="start", dag=dag)
    end_task = DummyOperator(task_id="end", dag=dag)
    get_input = PythonOperator(task_id="get_input", python_callable=get_ips)

    # Create graph
    start_task >> get_input >> end_task
