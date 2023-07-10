#!/usr/bin/env python3
"""
Python Version  : 3.10
* Name          : template_get_dag_runtime_stats.py
* Description   : DAG to fetch runtime stats for all registered DAGs
* Created       : 27-09-2022
"""

__author__ = "Paul Fry"
__version__ = "1.0"

from datetime import timedelta
from includes import common
import pendulum
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

# retrieve commonly used/shared variables
common_dag_vars = common.get_common_dag_vars(__file__)

dag_name = common_dag_vars["dag_name"]
# ------------------------------------------------------------------------------------
# DAG helpers code
# ------------------------------------------------------------------------------------
# to improve code readability, Python code is silo'd away in py_helpers
dag_helpers = common_dag_vars["dag_helpers"]
# similarly for better code readability, SQL code is silo'd away in sql_queries
sql_queries = common_dag_vars["sql_queries"]

# -------------------------------------------------------------------
# Input values
# -------------------------------------------------------------------
IP_DAG_DESCRIPTION = "Template Airflow DAG"  # TODO - update description
IP_DAG_TAGS = ["template"]  # TODO - update tags
IP_DAG_SCHEDULE = None  # TODO - update `schedule_interval`
IP_DAGRUN_TIMEOUT = timedelta(minutes=10)  # TODO - update `dagrun_timeout`
# best practice: set a value for dagrun_timeout as by default a value isn't provided.
# it's used to control the amount of time to allow for your DAG to run before failing.

with DAG(
    dag_id=dag_name,
    doc_md=common_dag_vars["doc_md"],  # best practice: render any README within the DAG folder
    default_args=common_dag_vars["default_args"],
    # note, re: dag execution - a dag run is triggered after the `start_date`+`schedule_interval`.
    start_date=pendulum.now(common_dag_vars["local_tz"]),
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

    # get all dags
    for selected_dag in common.get_dags():
        # note: don't include the current DAG (i.e., dag name = get_runtime_stats)
        if selected_dag != dag_name:
            # call get_dag_run_metadata
            get_dag_run_metadata = PythonOperator(
                task_id=f"get_dag_run_metadata_for_{selected_dag}",
                python_callable=dag_helpers.get_dag_run_metadata,
                op_kwargs={"dag_name": selected_dag},
                dag=dag,
            )

            # -------------------------------------------------------------------
            # Define task dependencies
            # -------------------------------------------------------------------
            start_task >> get_dag_run_metadata >> end_task
