#!/usr/bin/env python3
"""
Python Version  : 3.8
* Name          : template_dag.py
* Description   : Boilerplate Airflow task group script, w/o a context manager
*                 Reference: https://marclamberti.com/blog/airflow-taskgroups-all-you-need-to-know/
* Created       : 24-10-2022
"""

__author__ = "Paul Fry"
__version__ = "0.1"

import os
import sys
import importlib
import pendulum
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from airflow.utils.task_group import TaskGroup

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


with DAG(dag_id=dag_name, doc_md=doc_md, default_args=default_args, schedule_interval=None, tags=["example", "task_groups"]) as dag:

    # airflow tasks groups
    tg_parent_task_group = TaskGroup(group_id="tg_parent_task_group", dag=dag)
    tg_example = TaskGroup(group_id="tg_child_task_group", parent_group=tg_parent_task_group, dag=dag)

    # DAG tasks
    start_task = DummyOperator(task_id="start", task_group=tg_example)
    end_task = DummyOperator(task_id="end", task_group=tg_example)

    hello_world_task = PythonOperator(task_id="hello_world_task", python_callable=helpers.hello_world, task_group=tg_parent_task_group)

####################################################################
# DAG Lineage
####################################################################

start_task >> hello_world_task >> end_task
