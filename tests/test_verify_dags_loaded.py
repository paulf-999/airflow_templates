from airflow.models import DagBag


def test_verify_dags_loaded_without_errors():
    # validate there weren't any python lib import errors
    assert DagBag().import_errors == {}  # nosec
