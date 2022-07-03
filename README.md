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

---

## How-to run

### Local Airflow install

To create a local install of Airflow containing the prerequisite files, run `make`!

---

#### Scripted Airflow variable creation via CLI

To create an Airflow variable, add / change the entries listed in the Makefile recipe `create_airflow_variables`

#### Scripted Airflow connection creation via CLI

To create an Airflow connection, add / change the entries listed in the Makefile recipe `create_airflow_connections`

As well as containing a `Makefile` to script the install of a local Airflow instance, the `Makefile` shows the commands to script the creation of Airflow variables and connections.

---

## Airflow config `airflow.cfg`

Some of the Airflow config changes that have been applied include:

Note: Many of these changes have been applied/come from [this Medium.com blog post](https://medium.com/@agordienko/apache-airflow-cheatsheet-205f82d6edda).

| Config change | Config section | Description                  |
| -------| -----------------------------| ---- |
| dags_folder | core | To obviously point to the correct DAGs folder! |
| default_timezone | core | To use the local/desired timezone, as opposed to UTC |
| load_examples | core | This is set to `False` to prevent loading the examples |
| colored_console_log | logging | This is set to `False` to help resolve some Airflow logging errors produced |
| auth_backend | api | For local dev purposes, this is set to basic_auth. This allows API calls to be made without needing to generate tokens |
| default_ui_timezone | webserver | Similar to the 2nd point, this ensures the time used on the UI uses this timezone rather than UTC time |
| dag_default_view | webserver | I use the graph! Saves an extra click |
| min_file_process_interval | scheduler | Reduce the number of seconds Airflow waits to look for DAG changes. I set this to 5 for local dev work |
| dag_dir_list_interval | scheduler | Same as the above, I set this to 5 for the same reason. |
| catchup_by_default | scheduler | This value is set to `True` by default.  It means each time you unpause the DAG all the missed dagruns will start immediately. |
| hide_sensitive_variable_fields | admin | This is set to `True` to hide values from some variables. |

---

## Todo

* Investigate macros & parameters: https://marclamberti.com/blog/templates-macros-apache-airflow/

1. Done - Fetch DAG metadata.
2. Done - For a given DAG, get the corresponding TASK metadata
3. Done - Create task groups
4. In progress - Create unit tests
4. Not started - Use task decorators
5. Airflow templates

### Reading / links (note to self)

https://marclamberti.com/blog/templates-macros-apache-airflow/
https://stackoverflow.com/questions/46059161/airflow-how-to-pass-xcom-variable-into-python-function
