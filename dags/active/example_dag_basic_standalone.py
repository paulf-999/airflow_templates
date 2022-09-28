#!/usr/bin/env python3
"""
Python Version  : 3.10
* Name          : example_dag_basic.py
* Description   : Example Airflow DAG script.
* Created       : 28-09-2022
* Usage         : python3 example_dag.py
"""

__author__ = "Paul Fry"
__version__ = "1.0"

import os
import logging
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator

# from airflow.models import Variable

# Set up a specific logger with our desired output level
logging.basicConfig(format="%(message)s")
logger = logging.getLogger("airflow.task")
logger.setLevel(logging.INFO)

default_args = {"email": "email_eg@example.com", "owner": "airflow", "depends_on_past": False, "email_on_failure": False, "email_on_retry": False, "start_date": days_ago(1)}


def hello_world(**kwargs):

    print("Hello world")

    return


with DAG(dag_id=os.path.basename(__file__).replace(".py", ""), default_args=default_args, schedule_interval=None, tags=["template"]) as dag:

    start_task = DummyOperator(task_id="start", dag=dag)

    read_op_in_sub_tsk = PythonOperator(task_id="eg_task", python_callable=hello_world)

    end_task = DummyOperator(task_id="end", dag=dag)
