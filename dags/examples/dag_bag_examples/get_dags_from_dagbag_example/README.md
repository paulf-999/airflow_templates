## 'Get DAGs from `dag_bag` Example'

**Description**:    Example DAG showing how to retrieve all registered DAGs from Airflow's `dag_bag`.

**Date Created**:   24-11-2022

### Folder Contents

This directory describes the template Airflow DAG file/folder structure, as well as conventions used.

Where the purpose of each of the files within the template are as follows:

| Python file name | Description |
| ---------------- | ----------- |
| `dag.py` | The Airflow DAG file itself |
| `__dag_helpers.py` | For good housekeeping / code readability, this file is used to store Python code that may disturb readability within the DAG file file. This includes:<br/>* Python list variables that contain a long list of values<br/>* Python functions that are again quite long and disturb code readability|
| `__sql_queries.py` | Again for good housekeeping / code readability, all SQL queries are siloed / stored within this file and assigned to a variable.<br/>These variables are then referenced within the DAG file.<br/>Naming convention used for these variables: `__SQL_<VARIABLE_NAME__>`. |
