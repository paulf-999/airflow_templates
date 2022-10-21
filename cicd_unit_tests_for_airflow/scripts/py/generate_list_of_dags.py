import os

from airflow.models import DagBag

working_dir = os.path.join(os.getcwd(), "tests")

with open(os.path.join(working_dir, "tmp", "dags.txt"), "w") as op_file:
    for dag in DagBag().dags.values():
        op_file.write(f"{dag._dag_id}\n")
