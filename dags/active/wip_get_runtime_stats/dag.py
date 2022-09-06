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

dag = DAG(
    dag_id=dag_name,
    default_args=default_args,
    doc_md=doc_md,
    schedule_interval=None,
)

# with DAG(dag_id=dag_name, doc_md=doc_md, default_args=default_args, schedule_interval=None, tags=["template"]) as dag:

####################################################################
# DAG Operators
####################################################################
start_task = DummyOperator(task_id="start", dag=dag)
end_task = DummyOperator(task_id="end", dag=dag)

# TODO
# get_all_dags

# get_dag_runtime_stats = PythonOperator(task_id="get_dag_run_metadata", python_callable=helpers.get_dag_run_metadata, op_kwargs={"dag_name": "template_dag"})

for selected_dag in helpers.get_dags():
    # print(dag)

    if selected_dag != dag_name:
        # call get dag_run metadata
        get_dag_runtime_stats = PythonOperator(task_id=f"get_dag_run_metadata_for_{selected_dag}", python_callable=helpers.get_dag_run_metadata, op_kwargs={"dag_name": selected_dag}, dag=dag)

        ####################################################################
        # DAG Lineage
        ####################################################################
        start_task >> get_dag_runtime_stats >> end_task
        # start_task >> end_task


if __name__ == "__main__":
    # helpers.get_dag_run_metadata("template_dag")
    # helpers.get_dags()

    for my_dag in helpers.get_dags():
        print(my_dag)
        if my_dag != dag_name:

            # TODO:
            # call get dag_run metadata
            get_dag_run_metadata = PythonOperator(task_id=f"get_dag_run_metadata_for_{my_dag}", python_callable=helpers.get_dag_run_metadata, op_kwargs={"dag_name": my_dag})

            # TODO
            # get dag_run_task metadata

            # TODO
            # get DAG metadata
