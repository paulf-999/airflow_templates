import os

import pytest
from airflow.models import DagBag

dag_bag_list = []

# store all recognised DAGs in a list
with open(os.path.join(os.getcwd(), "tests", "tmp", "dags.txt")) as ip_file:
    for line in ip_file:
        dag_bag_list.append(line.strip())


@pytest.mark.parametrize("ip_dag_name", dag_bag_list)
def test_validate_start_date(ip_dag_name):
    dag = DagBag().get_dag(dag_id=ip_dag_name.strip())
    assert dag.default_args.get("start_date") is not None  # nosec


@pytest.mark.parametrize("ip_dag_name", dag_bag_list)
def test_verify_tags(ip_dag_name):
    dag = DagBag().get_dag(dag_id=ip_dag_name.strip())
    assert dag.tags is not None  # nosec


@pytest.mark.parametrize("ip_dag_name", dag_bag_list)
def test_validate_email(ip_dag_name):
    dag = DagBag().get_dag(dag_id=ip_dag_name.strip())
    assert dag.default_args.get("email") is not None  # nosec
