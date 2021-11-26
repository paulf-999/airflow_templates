#!/usr/bin/env python3
"""
Python Version  : 3.7
* Name          : get_dag_runtime_stats.py
* Description   : Boilerplate Airflow DAG script.
* Created       : 11-06-2021
"""

__author__ = "Paul Fry"
__version__ = "0.1"

import os
import sys
import logging
import importlib
import pendulum
from time import time
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator

# Set up a specific logger with our desired output level
logging.basicConfig(format="%(message)s")
logger = logging.getLogger("airflow.task")
logger.setLevel(logging.INFO)

local_tz = pendulum.timezone("Australia/Melbourne")

dagpath = os.path.dirname(os.path.abspath(__file__))
dagname = os.path.basename(dagpath)
dagroot = os.path.dirname(dagpath)

if dagroot not in sys.path:
    sys.path.append(dagroot)

helpers = importlib.import_module(".__dag_helpers", package=dagname)
queries = importlib.import_module(".__sql_queries", package=dagname)

default_args = {"owner": "airflow", "depends_on_past": False, "email_on_failure": False, "email_on_retry": False, "start_date": pendulum.now(local_tz).subtract(days=1)}

with DAG(dag_id=dagname, default_args=default_args, schedule_interval=None, tags=["template", "metadata"]) as dag:

    # operators here, e.g.:
    start_task = DummyOperator(task_id="start", dag=dag)

    get_dag_runtime_stats = PythonOperator(task_id="get_dag_runtime_stats", python_callable=helpers.get_dag_runtime_stats, provide_context=True)

    write_runtime_stats_to_sf = PythonOperator(task_id="write_runtime_stats_to_sf", python_callable=helpers.get_runtime_stats_dict, provide_context=True)

    end_task = DummyOperator(task_id="end", dag=dag)

# graph
start_task >> get_dag_runtime_stats >> write_runtime_stats_to_sf >> end_task
