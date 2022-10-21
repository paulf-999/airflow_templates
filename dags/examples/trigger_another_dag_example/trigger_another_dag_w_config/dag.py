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

dagpath = os.path.dirname(os.path.abspath(__file__))
dagname = os.path.basename(dagpath)
dagroot = os.path.dirname(dagpath)

if dagroot not in sys.path:
    sys.path.append(dagroot)

helpers = importlib.import_module(".__dag_helpers", package=dagname)
queries = importlib.import_module(".__sql_queries", package=dagname)

default_args = {"owner": "airflow", "depends_on_past": False, "email_on_failure": False, "email_on_retry": False, "start_date": pendulum.now(local_tz).subtract(days=1)}


with DAG(dag_id=dagname, default_args=default_args, schedule_interval=None, tags=["template"]) as dag:

    # operators here, e.g.:
    start_task = DummyOperator(task_id="start", dag=dag)
    end_task = DummyOperator(task_id="end", dag=dag)

    trigger = TriggerDagRunOperator(task_id="trigger_dagrun", trigger_dag_id="template_dag", conf={"param1": "abc", "param2": "xyz"})

# graph
start_task >> trigger >> end_task
