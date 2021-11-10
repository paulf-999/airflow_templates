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
from time import time
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.models import Variable
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

# TODOs
# confirm if def trigger() is needed? I think it's redundant
# 1) WIP - Fetch DAG metadata
# 2) Done - Create task groups
# 3) Not started - Use task decorators
# 4) Airflow templates & unit tests

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


def trigger(context, dag_run_obj):
    dag_run_obj.payload = {"message": context["dag_run"].conf["message"], "day": context["dag_run"].conf["day"]}
    return dag_run_obj


with DAG(dag_id=dagname, default_args=default_args, schedule_interval=None, tags=["template"]) as dag:

    # operators here, e.g.:
    start_task = DummyOperator(task_id="start", dag=dag)
    end_task = DummyOperator(task_id="end", dag=dag)

    hello_world_task = PythonOperator(task_id="hello_world_task", python_callable=helpers.hello_world, provide_context=True)

    gen_payload_eg = PythonOperator(task_id="hello_world_task", python_callable=helpers.get_context, provide_context=True)

    # send payload to 'get_dag_metadata' task
    # wip - need to first retrieve the payload (i.e. the conf ip) from the previous task
    send_payload_to_get_dag_metadata = TriggerDagRunOperator(task_id="trigger_get_metadata_dag", trigger_dag_id="wip_get_dag_metadata", conf={"dag_run_id": "template_dag"})

# graph
start_task >> hello_world_task >> gen_payload_eg >> send_payload_to_get_dag_metadata >> end_task
