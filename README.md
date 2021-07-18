# Overview (local Airflow)

Simple instructions for a local install of Airflow (see the `Makefile`).

To create a local install of Airflow containing the prerequisite files, run `make`!

---

## Contents

1. High-level summary
    * Example DAGs
2. How-to run
    * Local Airflow install
    * Scripted Airflow variable creation via CLI
    * Scripted Airflow connection creation via CLI

---

## 1. High-level summary

As well as containing a `Makefile` to script the install of a local Airflow instance, the `Makefile` shows the commands to script the creation of Airflow variables anc connections.

### Example DAGs

In addition, the repo contains 6 boilerplate Airflow DAGs, listed below:

1. `boilerplate_day.py`
2. `template_slack_post.py`
3. `template_task_failure_post_to_slack.py`
4. `template_mssql_query.py`
5. `template_eg_xcom_pull.py`
6. `template_dms_task_dag.py`

These make use of automated (scripted CLI commands) variable and connection creation.

---

## 2. How-to run

#### Local Airflow install

To create a local install of Airflow containing the prerequisite files, run `make`!

#### Scripted Airflow variable creation via CLI

To create an Airflow variable, add / change the entries listed in the Makefile recipe `create_airflow_variables`

#### Scripted Airflow connection creation via CLI

To create an Airflow connection, add / change the entries listed in the Makefile recipe `create_airflow_connections`

---

### Todo

* Investigate macros & parameters: https://marclamberti.com/blog/templates-macros-apache-airflow/

### Reading / links

https://marclamberti.com/blog/templates-macros-apache-airflow/
https://stackoverflow.com/questions/46059161/airflow-how-to-pass-xcom-variable-into-python-function
