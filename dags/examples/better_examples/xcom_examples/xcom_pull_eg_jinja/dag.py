#!/usr/bin/env python3
"""
Python Version  : 3.8
* Name          : template_dag.py
* Description   : Boilerplate Airflow DAG.
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
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from airflow.operators.bash import BashOperator

# Set up a specific logger with our desired output level
logging.basicConfig(format="%(message)s")
logger = logging.getLogger("airflow.task")
logger.setLevel(logging.INFO)

local_tz = pendulum.timezone("Australia/Melbourne")
dag_path = os.path.dirname(os.path.abspath(__file__))
dag_name = os.path.basename(dag_path)
dag_root = os.path.dirname(dag_path)

if dag_root not in sys.path:
    sys.path.append(dag_root)

helpers = importlib.import_module(".__dag_helpers", package=dag_name)
queries = importlib.import_module(".__sql_queries", package=dag_name)


def write_op():

    cmd = "example cmd"

    return cmd


default_args = {"owner": "airflow", "depends_on_past": False, "email_on_failure": False, "email_on_retry": False, "start_date": pendulum.now(local_tz).subtract(days=1)}

doc_md = helpers.try_render_readme(dag_path)

with DAG(dag_id=dag_name, doc_md=doc_md, default_args=default_args, schedule_interval=None, tags=["template"]) as dag:

    ####################################################################
    # DAG Operators
    ####################################################################
    start_task = DummyOperator(task_id="start")
    end_task = DummyOperator(task_id="end")

    py_op_eg = PythonOperator(task_id="py_op_eg", python_callable=write_op)

    xcom_pull_eg = BashOperator(task_id="xcom_pull_eg", bash_command="echo '{{ ti.xcom_pull(task_ids='py_op_eg') }}'")

####################################################################
# DAG Lineage
####################################################################
start_task >> py_op_eg >> xcom_pull_eg >> end_task
