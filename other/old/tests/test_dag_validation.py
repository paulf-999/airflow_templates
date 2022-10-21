import pytest
from airflow.models import DagBag


# Fixtures are used when we want to run some code before every test method.
# So instead of repeating the same code in every test we define fixtures.
@pytest.fixture()
def dag(pytestconfig):
    dag = DagBag().get_dag(dag_id=pytestconfig.getoption("dag_name"))
    return dag


# 'default_args' validation
def test_validate_start_date(dag):
    assert dag.default_args.get("start_date") is not None


def test_validate_email(dag):
    assert dag.default_args.get("email") is not None


# DAG arg validation
def test_verify_dag_id(dag):
    assert dag.dag_id is not None


def test_verify_tags(dag):
    assert dag.tags is not None
