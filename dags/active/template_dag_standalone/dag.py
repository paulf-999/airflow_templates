#!/usr/bin/env python3
"""
Python Version  : 3.10
* Name          : template_dag_standalone.py
* Description   : Boilerplate Airflow DAG. Doesn't use a shared/common package lib.
* Created       : 11-06-2021
"""

__author__ = "Paul Fry"
__version__ = "1.0"

import os
import sys
import importlib
from datetime import timedelta
import pendulum
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

# ------------------------------------------------------------------------------------
# setup and import the filepaths
# ------------------------------------------------------------------------------------
dag_path = os.path.dirname(os.path.abspath(__file__))  # filepath of the DAG
dag_name = os.path.basename(dag_path)  # name of the DAG (without the filepath)
dag_root = os.path.dirname(dag_path)  # path of all dags

if dag_root not in sys.path:
    sys.path.append(dag_root)

# ------------------------------------------------------------------------------------
# DAG helpers code
# ------------------------------------------------------------------------------------
# to improve code readability, Python code is silo'd away in py_helpers
py_helpers = importlib.import_module(".__dag_helpers", package=dag_name)
# similarly for better code readability, SQL code is silo'd away in sql_queries
sql_queries = importlib.import_module(".__sql_queries", package=dag_name)

# set local timezone
local_tz = pendulum.timezone("Europe/Dublin")

# attempt to render README file if it exists
doc_md = py_helpers.try_render_readme(dag_path)

# default/shared parameters used by all DAGs
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
}

with DAG(
    dag_name,
    description="Template Airflow DAG - standalone version",  # TODO - update description
    doc_md=doc_md,  # try to render a potential README.md within the DAG as a README for the DAG
    default_args=default_args,
    # note, re: dag execution - a dag run is triggered after the `start_date`+`schedule_interval`.
    start_date=pendulum.now(local_tz),
    schedule_interval=None,  # TODO - update `schedule_interval`
    dagrun_timeout=timedelta(minutes=10),  # TODO - update `dagrun_timeout`
    # best practice: set a value for dagrun_timeout as by default a value isn't provided.
    # it's used to control the amount of time to allow for your DAG to run before failing.
    catchup=False,  # best practice: set catchup=False to avoid accidental DAG run `backfilling`.
    tags=["template"],
) as dag:
    # -------------------------------------------------------------------
    # DAG tasks
    # -------------------------------------------------------------------
    start_task = EmptyOperator(task_id="start")
    end_task = EmptyOperator(task_id="end")

    hello_world_task = PythonOperator(task_id="hello_world_task", python_callable=py_helpers.hello_world)

# -------------------------------------------------------------------
# Define task dependencies
# -------------------------------------------------------------------
start_task >> hello_world_task >> end_task
