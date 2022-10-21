# How to Create DAG-Level Permissions

This code has been developed using the example described here - [Create Airflow roles with permissions from cli | Medium.com](https://towardsdatascience.com/create-airflow-roles-with-permissions-from-cli-64e05aaeb2fc).

First create an rbac role:

```python
python3 airflow_create_rbac_role.py \
    -u <airflow-url> \
    -r <name of role> \
    -d # <list of dags to enable access to, separated by spaces>
```

## Example usage

```python
python3 airflow_create_rbac_role.py \
    -u http://localhost:8080
    -r airflow_creator
    -d example_dag
```
