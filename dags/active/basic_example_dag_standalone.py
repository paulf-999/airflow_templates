#!/usr/bin/env python3
"""
Python Version  : 3.10
* Name          : basic_example_dag_standalone.py
* Description   : Example Airflow DAG script.
* Created       : 28-09-2022
* Usage         : python3 basic_example_dag_standalone.py
"""

__author__ = "Paul Fry"
__version__ = "1.0"

import os
import logging
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

# Set up a specific logger with our desired output level
logging.basicConfig(format="%(message)s")
logger = logging.getLogger("airflow.task")
logger.setLevel(logging.INFO)

dag_name = os.path.basename(__file__).replace(".py", "")
dag_tags = ["template"]

# default/shared parameters used by all DAGs
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
}


def hello_world(**kwargs):
    """example python function"""
    print("Hello world")

    return


with DAG(dag_id=dag_name, default_args=default_args, schedule_interval=None, tags=dag_tags) as dag:
    start_task = EmptyOperator(task_id="start", dag=dag)
    end_task = EmptyOperator(task_id="end", dag=dag)

    example_task = PythonOperator(task_id="hello_world_task", python_callable=hello_world)

# -------------------------------------------------------------------
# Define task dependencies
# -------------------------------------------------------------------
start_task >> example_task >> end_task
