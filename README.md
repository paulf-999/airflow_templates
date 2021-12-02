# Overview (local Airflow)

Simple instructions for a local install of Airflow (see the `Makefile`).

To create a local install of Airflow containing the prerequisite files, run `make`!

Note: `template_dag` is also timezone-aware (i.e., uses the python module `pendulum`).

---

## Contents

* How-to run
    * Local Airflow install
    * Running Airflow locally, post-install
    * Scripted Airflow variable creation via CLI
    * Scripted Airflow connection creation via CLI
* Example DAGs

---

## How-to run

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

As well as containing a `Makefile` to script the install of a local Airflow instance, the `Makefile` shows the commands to script the creation of Airflow variables anc connections.

---

### Example DAGs

In addition, the repo contains a number of example & template Airflow DAGs, listed below:

| DAG | Description                  |
| -------| -----------------------------|
| template_dag | Stripped back boilerplate/starting point to use for building a DAG. Makes use of pendulum, to make DAGs timezone-aware. |
| template_dag_w_get_metadata_trigger | Same as `template_dag`, except there's added functionality to trigger a separate DAG to get Airflow runtime metadata |
| template_dag_get_runtime_stats | Reusable Airflow DAG used to capture Airflow DAG runtime statistics/metadata at both the DAG and DAG-task level. |
| examples/ | Further example DAGs, e.g., showing `task_group` usage, showing how to trigger another DAG from within a DAG etc. |
| more_templates/ | Templated examples, e.g. templated snowflake operator, templated slack post, templated dbt calls etc. |

These make use of automated (scripted CLI commands) variable and connection creation.

---

## Todo

* Investigate macros & parameters: https://marclamberti.com/blog/templates-macros-apache-airflow/

1. Done - Fetch DAG metadata.
2. Done - For a given DAG, get the corresponding TASK metadata
3. Done - Create task groups
4. Not started - Use task decorators
5. Airflow templates & unit tests

### Reading / links (note to self)

https://marclamberti.com/blog/templates-macros-apache-airflow/
https://stackoverflow.com/questions/46059161/airflow-how-to-pass-xcom-variable-into-python-function
