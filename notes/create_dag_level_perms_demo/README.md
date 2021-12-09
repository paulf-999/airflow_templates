-- 1. create an rbac role
python3 airflow_create_rbac_role.py \
-u <airflow-url> \
-r <name of role> \
-d <list of dags to enable access to, separated by spaces>

-- example usage

python3 airflow_create_rbac_role.py -u http://localhost:8080 -r airflow_creator -d example_dag
