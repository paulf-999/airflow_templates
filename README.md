# Overview (local Airflow)

Simple instructions for a local install of Airflow.

To create a local install of Airflow containing the prerequisite files, run `make`!

# Example DAGs

There's currently 2 templated DAGs:

* `template_mssql_query.py`
* and `template_slack_post.py`

These make use of automated (scripted CLI commands) variable and connection creation. These are described below:

## Airflow variables

To create an Airflow variable, add / change the entries listed in the Makefile recipe `create_airflow_variables`

## Airflow connections 

To create an Airflow connection, add / change the entries listed in the Makefile recipe `create_airflow_connections`

# Todo:

* write mssql op to an s3 bucket???
* dbt eg
* Investigate macros & parameters: https://marclamberti.com/blog/templates-macros-apache-airflow/
## Reading / links

https://marclamberti.com/blog/templates-macros-apache-airflow/
