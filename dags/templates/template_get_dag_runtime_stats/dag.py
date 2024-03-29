#!/usr/bin/env python3
"""
Python Version  : 3.10
* Name          : template_get_dag_runtime_stats.py
* Description   : DAG to fetch runtime stats for all registered DAGs
* Created       : 27-09-2022
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
    start_task = DummyOperator(task_id="start", dag=dag)
    end_task = DummyOperator(task_id="end", dag=dag)

    # get_all_dags
    for selected_dag in common.get_dags():

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
