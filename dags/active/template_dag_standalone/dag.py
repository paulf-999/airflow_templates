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
import pendulum
from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator


def setup_file_paths():
    """Setup and import the filepaths"""
    dag_path = os.path.dirname(os.path.abspath(__file__))
    dag_name = os.path.basename(dag_path)
    dag_root = os.path.dirname(dag_path)

    if dag_root not in sys.path:
        sys.path.append(dag_root)

    return dag_path, dag_name, dag_root


# filepath setup
dag_path, dag_name, dag_root = setup_file_paths()

# to improve code readability, Python code is silo'd away in py_helpers
py_helpers = importlib.import_module(".__dag_helpers", package=dag_name)
# similarly for better code readability, SQL code is silo'd away in sql_queries
sql_queries = importlib.import_module(".__sql_queries", package=dag_name)

# set local timezone
local_tz = pendulum.timezone("Australia/Melbourne")

# attempt to render README file if it exists
doc_md = py_helpers.try_render_readme(dag_path)

# default/shared parameters used by all DAGs
default_args = {"owner": "airflow", "depends_on_past": False, "email_on_failure": False, "email_on_retry": False}

with DAG(
    dag_name,
    description="Template Airflow DAG - standalone version",
    doc_md=doc_md,  # try to render any potential README.md file within the DAG repo as the README for the DAG
    default_args=default_args,
    # note, re: 'dag execution' using the `start_date` & `schedule_interval` params.
    # A DAG is triggered after the `start_date` AND the `schedule_interval`.
    start_date=pendulum.now(local_tz),
    schedule_interval=None,  # TODO - update `schedule_interval`
    # TODO - update `dagrun_timeout`
    # best practice is to provide a value for `dagrun_timeout`
    # by default a value isn't provided.
    # `dagrun_timeout` is used to control the amount of time to allow for your DAG to run before failing.
    dagrun_timeout=timedelta(minutes=10),
    catchup=False,  # best practice is to set this value to false. As otherwise, Airflow will try to trigger all pending dagruns.
    tags=["template"]
) as dag:

    ####################################################################
    # DAG Operators
    ####################################################################
    start_task = DummyOperator(task_id="start")
    end_task = DummyOperator(task_id="end")

    hello_world_task = PythonOperator(task_id="hello_world_task", python_callable=py_helpers.hello_world)

####################################################################
# DAG Lineage
####################################################################
start_task >> hello_world_task >> end_task
