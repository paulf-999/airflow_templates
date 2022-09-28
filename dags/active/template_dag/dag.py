#!/usr/bin/env python3
"""
Python Version  : 3.10
* Name          : template_dag.py
* Description   : Boilerplate Airflow DAG, fetching attributes from a shared Airflow package
* Created       : 28-09-2022
"""

__author__ = "Paul Fry"
__version__ = "1.0"

from includes import common
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator

dag_name, dag_helpers, sql_queries, doc_md, logger, local_tz, default_args = common.get_common_dag_vars(__file__)  # noqa

with DAG(dag_id=dag_name, doc_md=doc_md, default_args=default_args, schedule_interval=None, tags=["template"]) as dag:

    ####################################################################
    # DAG Operators
    ####################################################################
    start_task = DummyOperator(task_id="start")
    end_task = DummyOperator(task_id="end")

    hello_world_task = PythonOperator(task_id="hello_world_task", python_callable=dag_helpers.hello_world)

####################################################################
# DAG Lineage
####################################################################
start_task >> hello_world_task >> end_task
