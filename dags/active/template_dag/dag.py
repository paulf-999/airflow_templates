#!/usr/bin/env python3
"""
Python Version  : 3.10
* Name          : template_dag.py
* Description   : Boilerplate Airflow DAG, fetching attributes from a shared Airflow package
* Created       : 28-09-2022
"""

__author__ = "Paul Fry"
__version__ = "1.0"

from datetime import timedelta
from includes import common
import pendulum
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

# retrieve commonly used/shared variables
common_dag_vars = common.get_common_dag_vars(__file__)

# ------------------------------------------------------------------------------------
# DAG helpers code
# ------------------------------------------------------------------------------------
# to improve code readability, Python code is silo'd away in py_helpers
dag_helpers = common_dag_vars["dag_helpers"]
# similarly for better code readability, SQL code is silo'd away in sql_queries
sql_queries = common_dag_vars["sql_queries"]

# -------------------------------------------------------------------
# Input values
# -------------------------------------------------------------------
IP_DAG_DESCRIPTION = "Template Airflow DAG"  # TODO - update description
IP_DAG_TAGS = ["template"]  # TODO - update tags
IP_DAG_SCHEDULE = None  # TODO - update `schedule_interval`
IP_DAGRUN_TIMEOUT = timedelta(minutes=10)  # TODO - update `dagrun_timeout`
# best practice: set a value for dagrun_timeout as by default a value isn't provided.
# it's used to control the amount of time to allow for your DAG to run before failing.

with DAG(
    dag_id=common_dag_vars["dag_name"],
    description=IP_DAG_DESCRIPTION,
    doc_md=common_dag_vars["doc_md"],  # best practice: render any README within the DAG folder
    default_args=common_dag_vars["default_args"],
    # note, re: dag execution - a dag run is triggered after the `start_date`+`schedule_interval`.
    start_date=pendulum.now(common_dag_vars["local_tz"]),
    schedule_interval=IP_DAG_SCHEDULE,
    dagrun_timeout=IP_DAGRUN_TIMEOUT,
    catchup=False,  # best practice: set catchup=False to avoid accidental DAG run `backfilling`.
    tags=IP_DAG_TAGS,
) as dag:
    # -------------------------------------------------------------------
    # DAG tasks
    # -------------------------------------------------------------------
    start_task = EmptyOperator(task_id="start")
    end_task = EmptyOperator(task_id="end")

    hello_world_task = PythonOperator(task_id="hello_world_task", python_callable=common.hello_world)

# -------------------------------------------------------------------
# Define task dependencies
# -------------------------------------------------------------------
start_task >> hello_world_task >> end_task
