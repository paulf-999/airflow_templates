# WIP - Overview (local Airflow)

Simple instructions for a local install of Airflow.

To create a local install of Airflow containing the prerequisite files, run `make`!

# Example DAGs

There are currently 6 template DAGs:

1. `boilerplate_day.py`
2. `template_slack_post.py`
3. `template_task_failure_post_to_slack.py`
4. `template_mssql_query.py`
5. `template_eg_xcom_pull.py`
6. `template_dms_task_dag.py`

These make use of automated (scripted CLI commands) variable and connection creation. These are described below:

## Airflow variables

To create an Airflow variable, add / change the entries listed in the Makefile recipe `create_airflow_variables`

## Airflow connections

To create an Airflow connection, add / change the entries listed in the Makefile recipe `create_airflow_connections`

# Todo:

* Investigate macros & parameters: https://marclamberti.com/blog/templates-macros-apache-airflow/
## Reading / links

https://marclamberti.com/blog/templates-macros-apache-airflow/
https://stackoverflow.com/questions/46059161/airflow-how-to-pass-xcom-variable-into-python-function
