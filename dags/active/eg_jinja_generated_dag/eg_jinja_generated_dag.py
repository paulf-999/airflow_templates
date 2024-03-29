#!/usr/bin/env python3
"""
Python Version  : 3.10
* Name          : eg_jinja_generated_dag.py
* Description   : Example Airflow DAG script.
* Created       : 28-09-2022
* Usage         : python3 example_dag.py
"""

__author__ = "Paul Fry"
__version__ = "1.0"

import os
import sys
import logging
import importlib
from datetime import timedelta
import pendulum
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator


# Set up a specific logger with our desired output level
logging.basicConfig(format="%(message)s")
logger = logging.getLogger("airflow.task")
logger.setLevel(logging.INFO)


def hello_world(**kwargs):
    """Example python function"""
    print("Hello world")

    return


def setup_file_paths():
    """Setup and import the filepaths"""
    dag_path = os.path.dirname(os.path.abspath(__file__))
    dag_root = os.path.dirname(dag_path)

    if dag_root not in sys.path:
        sys.path.append(dag_root)

    return dag_path, dag_root


# filepath setup
dag_path, dag_root = setup_file_paths()

# to improve code readability, Python code is silo'd away in py_helpers
py_helpers = importlib.import_module(".__dag_helpers", package="eg_jinja_generated_dag")
# similarly for better code readability, SQL code is silo'd away in sql_queries
sql_queries = importlib.import_module(".__sql_helpers", package="eg_jinja_generated_dag")

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
    "eg_jinja_generated_dag",
    description="Template Airflow DAG - standalone version",
    doc_md=doc_md,  # try to render any potential README.md file within the DAG repo as the README for the DAG
    default_args=default_args,
    # note, re: dag execution - a dag run is triggered after the `start_date`+`schedule_interval`.
    start_date=pendulum.now(local_tz),
    schedule_interval=None,
    catchup=False,  # best practice - set this to `False` to have full control of your DAG and avoid accidental `backfilling`.
    tags=["example_tag1", "tag2"],
    # best practice is to provide a value for `dagrun_timeout` as by default a value isn't provided.
    # `dagrun_timeout` is used to control the amount of time to allow for your DAG to run before failing.
    dagrun_timeout=timedelta(minutes=10),
) as dag:
    # -------------------------------------------------------------------
    # DAG tasks
    # -------------------------------------------------------------------
    start_task = EmptyOperator(task_id="start")
    end_task = EmptyOperator(task_id="end")

    hello_world_task = PythonOperator(
        task_id="hello_world_task", python_callable=py_helpers.hello_world
    )

# -------------------------------------------------------------------
# Define task dependencies
# -------------------------------------------------------------------
start_task >> hello_world_task >> end_task
