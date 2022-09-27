#!/usr/bin/env python3
"""
Python Version  : 3.8
* Name          : get_dag_runtime_stats.py
* Description   : DAG to fetch runtime stats for all registered DAGs
* Created       : 27-09-2022
"""

__author__ = "Paul Fry"
__version__ = "0.1"

from includes import common
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator

dag_name, dag_helpers, sql_queries, doc_md, logger, local_tz, default_args = common.get_common_dag_vars(__file__)  # noqa

dag = DAG(
    dag_id=dag_name,
    default_args=default_args,
    doc_md=doc_md,
    schedule_interval=None,
)

####################################################################
# DAG Operators
####################################################################
start_task = DummyOperator(task_id="start", dag=dag)
end_task = DummyOperator(task_id="end", dag=dag)

# get_all_dags
for selected_dag in dag_helpers.get_dags():

    # note: don't include the current DAG (get_runtime_stats)
    if selected_dag != dag_name:
        # call get dag_run metadata
        # fmt: off
        get_dag_run_metadata = PythonOperator(
            task_id=f"get_dag_run_metadata_for_{selected_dag}",
            python_callable=dag_helpers.get_dag_run_metadata,
            op_kwargs={"dag_name": selected_dag},
            dag=dag
        )
        # fmt: on

        ####################################################################
        # DAG Lineage
        ####################################################################
        start_task >> get_dag_run_metadata >> end_task
