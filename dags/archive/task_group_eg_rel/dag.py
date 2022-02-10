#!/usr/bin/env python3
"""
Python Version  : 3.7
* Name          : template_dag.py
* Description   : Boilerplate Airflow task group script. Reference: http://airflow.apache.org/docs/apache-airflow/2.0.1/_modules/airflow/example_dags/example_task_group.html
* Created       : 11-06-2021
* Usage         : python3 task_group_eg.py
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
from airflow.utils.task_group import TaskGroup
from airflow.models import Variable
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
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


with DAG(dag_id=dagname, default_args=default_args, schedule_interval=None, tags=["template"]) as dag:

    # operators here, e.g.:
    start_task = DummyOperator(task_id="start", dag=dag)

    with TaskGroup("extract", tooltip="extract") as extract:

        with TaskGroup("get_instore_data", tooltip="get_instore_data") as get_instore_data:
            task_1 = BashOperator(task_id="store_1", bash_command="echo 1")
            task_2 = BashOperator(task_id="store_2", bash_command="echo 1")
            task_3 = DummyOperator(task_id="task_3")

        with TaskGroup("get_online_data", tooltip="get_online_data") as get_online_data:
            task_1 = BashOperator(task_id="store_1", bash_command="echo 1")
            task_2 = BashOperator(task_id="task_2", bash_command="echo 1")
            task_3 = DummyOperator(task_id="task_3")

    with TaskGroup("transform", tooltip="transform") as transform:

        with TaskGroup("join_customer_data", tooltip="join_customer_data") as join_customer_data:
            task_2 = BashOperator(task_id="task_2", bash_command="echo 1")
            task_3 = DummyOperator(task_id="task_3")
            task_4 = DummyOperator(task_id="task_4")

        with TaskGroup("join_transaction_data", tooltip="join_transaction_data") as join_transaction_data:
            task_2 = BashOperator(task_id="task_2", bash_command="echo 1")
            task_3 = DummyOperator(task_id="task_3")
            task_4 = DummyOperator(task_id="task_4")

            [task_2, task_3] >> task_4

    with TaskGroup("load", tooltip="load") as load:
        task_1 = BashOperator(task_id="load_task", bash_command="echo 1")
        task_2 = BashOperator(task_id="load_task2", bash_command="echo 1")
        task_3 = BashOperator(task_id="load_task3", bash_command="echo 1")

        task_1 >> task_2 >> task_3

    end_task = DummyOperator(task_id="end", dag=dag)

    # graph
    start_task >> extract >> transform >> load >> end_task
