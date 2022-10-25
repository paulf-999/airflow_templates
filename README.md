# Airflow Templates

This repo contains:

* A collection of template and example Airflow DAGs I've collated over time.
* As well as a (local) Airflow build script (see `Makefile`).
* Scripts to implement CICD unit tests for Airflow DAGs (see `cicd_unit_tests_for_airflow`).

---

## Contents

1. Template and Example DAGs
2. Local Airflow Build Script
3. CICD Unit Tests for Airflow (docs are WIP)
4. Airflow Config `airflow.cfg`

---

### 1. Template and Example DAGs

See the parent folder `dags` for a collection of template & example DAGs that I've collated over time.

### 2. Local Airflow Build Script

* See `Makefile` at the project root
* This `Makefile` provides a simple way of creating a local install of Airflow.
* To create a local install of Airflow you need to:
  * Edit the input args listed in `ip/config.json`'
  * Then run `make installations`

### 3. CICD Unit Tests for Airflow (docs are WIP)

* See the parent folder `cicd_unit_tests_for_airflow`
* This folder consists of all the files required to implement and trigger Airflow unit tests as part of any GitLab CI build
* See `cicd_unit_tests_for_airflow/.gitlab-ci` for the commands/args used to:
  * Launch an Airflow instance (in standalone mode) within a CI job
  * Perform Airflow (pytest) unit tests
* See `cicd_unit_tests_for_airflow/tests/` to see the code used for the pytests used for Airflow DAGs.

---

### 4. Airflow Config `airflow.cfg`

Some of the Airflow config changes that I commonly make (and have made for the local build script) are listed below.

Note: Many of these changes have been applied/come from [this Medium.com blog post](https://medium.com/@agordienko/apache-airflow-cheatsheet-205f82d6edda).

| Config change | Config section | Description                  |
| -------| -----------------------------| ---- |
| dags_folder | core | To obviously point to the correct DAGs folder! |
| default_timezone | core | To use the local/desired timezone, as opposed to UTC |
| load_examples | core | This is set to `False` to prevent loading the examples |
| hide_sensitive_variable_fields | core | This is set to `True` to hide values from some variables. |
| colored_console_log | logging | This is set to `False` to help resolve some Airflow logging errors produced |
| auth_backend | api | For local dev purposes, this is set to basic_auth. This allows API calls to be made without needing to generate tokens |
| default_ui_timezone | webserver | Similar to the 2nd point, this ensures the time used on the UI uses this timezone rather than UTC time |
| dag_default_view | webserver | I use the graph! Saves an extra click |
| min_file_process_interval | scheduler | Reduce the number of seconds Airflow waits to look for DAG changes. I set this to 5 for local dev work |
| dag_dir_list_interval | scheduler | Same as the above, I set this to 5 for the same reason. |
| catchup_by_default | scheduler | This value is set to `True` by default.  It means each time you unpause the DAG all the missed dagruns will start immediately. |
