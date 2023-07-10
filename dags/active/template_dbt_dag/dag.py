#!/usr/bin/env python3
"""
Python Version  : 3.8
* Name          : template_dbt_dag.py
* Description   : Boilerplate Airflow DAG for interacting with dbt.
* Created       : 11-06-2021
"""

__author__ = "Paul Fry"
__version__ = "0.1"

import os
import sys
from datetime import timedelta
import importlib
import pendulum
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator

dag_path = os.path.dirname(os.path.abspath(__file__))
dag_name = os.path.basename(dag_path)
dag_root = os.path.dirname(dag_path)

if dag_root not in sys.path:
    sys.path.append(dag_root)

# -------------------------------------------------------------------
# Input values
# -------------------------------------------------------------------
DBT_PROJECT_DIR = "<PATH TO DBT_PROJECT_FOLDER>"  # TODO - update filepath

IP_LOCAL_TZ = pendulum.timezone("Europe/Dublin")  # set local timezone
IP_DAG_DESCRIPTION = "Template Airflow DAG"  # TODO - update description
IP_DAG_TAGS = ["template"]  # TODO - update tags
IP_DAG_SCHEDULE = None  # TODO - update `schedule_interval`
IP_DAGRUN_TIMEOUT = timedelta(minutes=10)  # TODO - update `dagrun_timeout`
# best practice: set a value for dagrun_timeout as by default a value isn't provided.
# it's used to control the amount of time to allow for your DAG to run before failing.

# ------------------------------------------------------------------------------------
# DAG helpers code
# ------------------------------------------------------------------------------------
# to improve code readability, Python code is silo'd away in py_helpers
helpers = importlib.import_module(".__dag_helpers", package=dag_name)
# similarly for better code readability, SQL code is silo'd away in sql_queries
queries = importlib.import_module(".__sql_queries", package=dag_name)
# attempt to render README file if it exists
doc_md = helpers.try_render_readme(dag_path)

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "start_date": pendulum.now(IP_LOCAL_TZ).subtract(days=1),
}


with DAG(
    dag_id=dag_name,
    description=IP_DAG_DESCRIPTION,
    doc_md=doc_md,
    default_args=default_args,
    start_date=pendulum.now(IP_LOCAL_TZ),
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

    dbt_command = BashOperator(
        task_id="dbt_conn_test",
        bash_command=f"set -e; cd {DBT_PROJECT_DIR}; dbt debug --profiles-dir profiles",
    )


# -------------------------------------------------------------------
# Define task dependencies
# -------------------------------------------------------------------
start_task >> dbt_command >> end_task
