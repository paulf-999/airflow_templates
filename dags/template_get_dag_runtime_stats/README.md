# Template 'get DAG runtime stats' Airflow DAG

Template / reusable Airflow DAG used to capture Airflow DAG runtime statistics/metadata at both the DAG and DAG-task level.

---

## Contents

* High-level summary
* How-to use

---

## High-level summary

This reusable Airflow dag is designed to be itself called by a 'parent' DAG, to capture statistics/metadata relating to the Airflow dag run.

## How-to use

In order to make use of this within your existing Airflow dags, you'll need to:

1. Within your Airflow DAG, create a new Airflow task that uses the 'TriggerDagRunOperator'. This module can be imported using:
`from airflow.operators.trigger_dagrun import TriggerDagRunOperator`
2. In this new task, you'll need to pass in DAG configuration to specify the name of your 'source dag' (i.e., the dag you wish to retrieve runtime stats/metadata about). This is done by passing the following arg to the `TriggerDagRunOperator` task
`conf={"source_dag": "<source dag name here>", "target_tbl": "<target table name here>"}`.

### Example

Shown below is an example of a new task you would create in your existing Airflow DAG, to invoke the 'template_get_dag_runtime_stats' dag:

`trigger_get_dag_metadata_dag = TriggerDagRunOperator(task_id="trigger_get_metadata_dag", trigger_dag_id="template_get_dag_runtime_stats", conf={"source_dag": "<source dag name here>", "target_tbl": "<target table name here>"}`
