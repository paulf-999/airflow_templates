import os
import re

import pytest

dag_bag_list = []

# store all recognised DAGs in a list
with open(os.path.join(os.getcwd(), "tests", "tmp", "dags.txt")) as ip_file:
    for line in ip_file:
        dag_bag_list.append(line.strip())


# Valid DAG names should only contain (lower-case) alphanumeric characters and underscores
# They shouldn't contain whitespace, dashes or dots
@pytest.mark.parametrize("ip_dag_name", dag_bag_list)
def test_verify_dag_name_is_valid(ip_dag_name):
    valid_dag_name_pattern = "^[^- .][a-z_1-9]*$"
    assert re.match(valid_dag_name_pattern, ip_dag_name)  # nosec
