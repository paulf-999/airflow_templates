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
import pendulum
from datetime import timedelta
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator

# retrieve commonly used/shared variables
dag_name, dag_helpers, sql_queries, doc_md, logger, local_tz, default_args = common.get_common_dag_vars(__file__)  # noqa

with DAG(
    dag_name,
    description="Template Airflow DAG",
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

    hello_world_task = PythonOperator(task_id="hello_world_task", python_callable=common.hello_world)

####################################################################
# DAG Lineage
####################################################################
start_task >> hello_world_task >> end_task
