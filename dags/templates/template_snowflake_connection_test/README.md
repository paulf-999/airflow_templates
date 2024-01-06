## Template Airflow DAG - Standalone Version

**Description**:    Template Airflow DAG. Note: this is a standalone version of [template_dag](https://github.com/paulf-999/airflow_templates/tree/main/dags/active/template_dag_standalone), with the difference being that this version doesn't make use of shared/common code.

**Date Created**:   24-11-2022

### Folder Contents

This directory describes the template Airflow DAG file/folder structure, as well as conventions used.

Where the purpose of each of the files within the template are as follows:

| Python file name | Description |
| ---------------- | ----------- |
| `dag.py` | The Airflow DAG file itself |
| `__dag_helpers.py` | For good housekeeping / code readability, this file is used to store Python code that may disturb readability within the DAG file file. This includes:<br/>* Python list variables that contain a long list of values<br/>* Python functions that are again quite long and disturb code readability|
| `__sql_queries.py` | Again for good housekeeping / code readability, all SQL queries are siloed / stored within this file and assigned to a variable.<br/>These variables are then referenced within the DAG file.<br/>Naming convention used for these variables: `__SQL_<VARIABLE_NAME__>`. |
