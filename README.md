# Airflow Templates

This repo contains:

* A collection of template/example Airflow DAGs I've collated over time.
* A local Airflow build script, using Astro CLI (see `Makefile`).
* CICD unit tests for Airflow DAGs (see [src/cicd_unit_tests_for_airflow](src/cicd_unit_tests_for_airflow)).

---

## Contents

1. Template/Example DAGs
2. Local Airflow Build Script
3. CICD Unit Tests for Airflow (docs are WIP)
4. Airflow Config `airflow.cfg`

---

### 1. Template/Example DAGs

See the parent folder `dags` for a collection of template & example DAGs that I've collated over time.

### 2. Local Airflow Build Script

* See `Makefile` at the project root
* This `Makefile` provides a simple way of creating a local install of Airflow.
* To create a local install of Airflow you need to:
  * Edit the value for `ASTRO_PROJECT_NAME` on line 24 in the `Makefile`
  * Then run `make installations`

### 3. CICD Unit Tests for Airflow (docs are WIP)

* See [src/cicd_unit_tests_for_airflow](src/cicd_unit_tests_for_airflow).
* This folder consists of all the files required to implement and trigger Airflow unit tests as part of any GitLab CI build
* See `cicd_unit_tests_for_airflow/.gitlab-ci` for the commands/args used to:
  * Launch an Airflow instance (in standalone mode) within a CI job
  * Perform Airflow (pytest) unit tests
* See `cicd_unit_tests_for_airflow/tests/` to see the code used for the pytests used for Airflow DAGs.

---

### 4. Airflow Config `airflow.cfg`

Some of the Airflow config changes that I commonly make (and have made for the local build script) are listed below.

Note: Many of these changes have been applied/come from [this Medium.com blog post](https://medium.com/@agordienko/apache-airflow-cheatsheet-205f82d6edda).

| Config change                    | Config section | Value | Description |
| ---------------------------------| ---------------| ----  | ---- |
| dags_folder                      | core           | <path to your dags folder> |To obviously point to the correct DAGs folder! |
| default_timezone                 | core           | <desired_timezone> | To use the local/desired timezone, as opposed to UTC. |
| load_examples                    | core           | `False` | Set to `False` to prevent loading the examples. |
| hide_sensitive_variable_fields   | core           | `True` | Set to `True` to prevent the value of a variable from beong displayed. |
| colored_console_log              | logging        | `False` | Set to `False` to help resolve Airflow logging errors. |
| auth_backend                     | api            | `basic_auth` | For local dev purposes, this is set to basic_auth. This allows API calls to be made without needing to generate tokens. |
| default_ui_timezone              | webserver      | <desired_timezone> | Similar to the 2nd point, this ensures the time used on the UI uses this timezone rather than UTC time. |
| dag_default_view                 | webserver      | `graph` | I use the graph! Saves an extra click. |
| min_file_process_interval        | scheduler      | `5` | Reduce the number of seconds Airflow waits to look for DAG changes. I set this to 5 for local dev work. |
| dag_dir_list_interval            | scheduler      | `5` | Same as the above, I set this to 5 for the same reason. |
| catchup_by_default               | scheduler      | `False` | Set to `False` as by default, it is set to `True`. Setting it to true means each time you unpause the DAG all the missed dagruns will start immediately. |
