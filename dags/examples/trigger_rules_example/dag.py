#!/usr/bin/env python3
"""
Python Version  : 3.10
* Name          : template_dag_standalone.py
* Description   : Example showing how trigger rules work. Source: https://marclamberti.com/blog/airflow-trigger-rules-all-you-need-to-know/
* Created       : 11-06-2021
"""

__author__ = "Paul Fry"
__version__ = "1.0"

import os
import sys
import logging
import importlib
import pendulum
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator

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

default_args = {"owner": "airflow", "depends_on_past": False, "email_on_failure": False, "email_on_retry": False, "start_date": pendulum.now(local_tz).subtract(days=1)}

doc_md = helpers.try_render_readme(dag_path)


def cause_failure_eg(**kwargs):

    assert "a" == "b"

    return


with DAG(dag_id=dag_name, doc_md=doc_md, default_args=default_args, schedule_interval=None, tags=["template"]) as dag:

    ####################################################################
    # DAG Operators
    ####################################################################
    start_task = DummyOperator(task_id="start")
    end_task = DummyOperator(task_id="end")

    cause_failure_eg = PythonOperator(task_id="cause_failure_eg", python_callable=cause_failure_eg)

    #
    task_failed_eg = DummyOperator(task_id="task_failed_eg", trigger_rule="one_failed")

####################################################################
# DAG Lineage
####################################################################
start_task >> cause_failure_eg >> task_failed_eg >> end_task
