## Airflow DAG Template - including step to fetch DAG metadata

This diretory describes the template Airflow DAG file/folder structure, as well as conventions used.

Where the purpose of each of the files within the template are as follows:

| Python file name | Description |
| ---------------- | ----------- |
| `__dag_helpers.py` | For good housekeeping / code readability, this file is used to store Python code that may disturb readability within the DAG file file. This includes:<br/>* Python list variables that contain a long list of values<br/>* Python functions that are again quite long and disturb code readability|
| `__sql_queries.py` | Again for good housekeeping / code readability, all SQL queries are siloed / stored within this file and assigned to a variable.<br/>These variables are then referenced within the DAG file.<br/>Naming convention used for these variables: `__SQL_<VARIABLE_NAME__>`. |
| `day.py` | The Airflow DAG file itself |
