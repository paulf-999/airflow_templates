#!/usr/bin/env python3
"""
Python Version  : 3.7
* Name          : template_dag.py
* Description   : Boilerplate Airflow DAG script.
* Created       : 11-06-2021
* Usage         : python3 template_dag.py
"""

__author__ = "Paul Fry"
__version__ = "0.1"

import os
import sys
import logging
import importlib
import pendulum
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

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


with DAG(dag_id=dag_name, default_args=default_args, schedule_interval=None, tags=["example", "trigger_another_dag"]) as dag:

    # operators here, e.g.:
    start_task = DummyOperator(task_id="start", dag=dag)
    end_task = DummyOperator(task_id="end", dag=dag)

    trigger = TriggerDagRunOperator(
        task_id="trigger_dagrun",
        trigger_dag_id="template_dag",
        execution_date='{{ ds }}',  # best practice: date passed here will be used as the date used by the triggered dag
        wait_for_completion=True,  # best practice: if you want to wait for triggered DAG to complete before progressing to the next task.
        poke_interval=60,  # interval of frequency time to check whether triggered dag is complete
        reset_dag_run=True,  # best practice: without this arg, you won't be able to backfill/rerun your dag. Default value=False.
        failed_states=["failed"]  # best practice: without this arg, you're triggered dag will continue to run
    )

# graph
start_task >> trigger >> end_task
