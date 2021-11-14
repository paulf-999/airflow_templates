# Overview (local Airflow)

Simple instructions for a local install of Airflow (see the `Makefile`).

To create a local install of Airflow containing the prerequisite files, run `make`!

Note: boilerplate_dag is also timezone-aware (i.e., uses the python module 'pendulum').

---

## Contents

1. High-level summary
    * Example DAGs
2. How-to run
    * Local Airflow install
    * Running Airflow locally, post-install
    * Scripted Airflow variable creation via CLI
    * Scripted Airflow connection creation via CLI

---

## 1. High-level summary

As well as containing a `Makefile` to script the install of a local Airflow instance, the `Makefile` shows the commands to script the creation of Airflow variables anc connections.

### Example DAGs

In addition, the repo contains 6 boilerplate Airflow DAGs, listed below:

| DAG | Description                  |
| -------| -----------------------------|
| template_dag | Stripped back boilerplate/starting point to use for building a DAG. Makes use of pendulum, to make DAGs timezone-aware. |
| template_slack_post.py | Cut back example showing the syntax needed to write to Slack from Airflow. |
| template_task_failure_post_to_slack.py | Extends the above example, to instead post to Slack upon any task failing within an Airflow DAG. |
| template_mssql_query.py | Demonstrates the syntax needed to perform an MSSQL query. |
| template_eg_xcom_pull.py | Example of using XCom to retrieve the output of previous Airflow tasks. |
| template_dms_task_dag.py | Integrates with AWS DMS to check and invoke a DMS job. |
| template_dbt_dag.py | Integrates with DBT to run a DBT test, then DBT run command. |

These make use of automated (scripted CLI commands) variable and connection creation.

---

## 2. How-to run

### Local Airflow install

To create a local install of Airflow containing the prerequisite files, run `make`!

### Running Airflow locally, post-install

To subsequently run Airflow (post-install), do the following:

* In a terminal window, navigate to the Git repo root and enter `make start_webserver`
* In another terminal window, navigate to the Git repo root and enter `make start_scheduler`

### Scripted Airflow variable creation via CLI

To create an Airflow variable, add / change the entries listed in the Makefile recipe `create_airflow_variables`

#### Scripted Airflow connection creation via CLI

To create an Airflow connection, add / change the entries listed in the Makefile recipe `create_airflow_connections`

---

## Todo

* Investigate macros & parameters: https://marclamberti.com/blog/templates-macros-apache-airflow/

1. Done - Fetch DAG metadata.
2. WIP - For a given DAG, get the corresponding TASK metadata
3. Done - Create task groups
4. Not started - Use task decorators
5. Airflow templates & unit tests

### Reading / links (note to self)

https://marclamberti.com/blog/templates-macros-apache-airflow/
https://stackoverflow.com/questions/46059161/airflow-how-to-pass-xcom-variable-into-python-function
