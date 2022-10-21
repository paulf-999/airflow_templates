import argparse
from typing import List

import requests


def create_rbac_role_with_permissions(
    airflow_url: str,
    new_role_name: str,
    dag_names: List[str],
):
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    read = "can_read"
    edit = "can_edit"
    create = "can_create"
    delete = "can_delete"
    menu = "menu_access"

    r_list = ["Task Instances", "Website", "DAG Runs", "Audit Logs", "ImportError", "XComs", "DAG Code", "Plugins", "My Password", "My Profile", "Jobs", "SLA Misses", "DAG Dependencies", "Task Logs"]

    # add general permissions
    permissions = []
    read_permissions = make_permissions(read, r_list)
    edit_permissions = make_permissions(edit, ["Task Instances", "My Password", "My Profile", "DAG Runs"])
    create_permissions = make_permissions(create, ["DAG Runs", "Task Instances"])
    delete_permissions = make_permissions(delete, ["DAG Runs", "Task Instances"])
    menu_permissions = make_permissions(menu, ["View Menus", "Browse", "Docs", "Documentation", "SLA Misses", "Jobs", "DAG Runs", "Audit Logs", "Task Instances", "DAG Dependencies"])
    permissions += read_permissions + edit_permissions + create_permissions + delete_permissions + menu_permissions

    # add dag-specific permissions
    for dag in dag_names:
        dag = "DAG:" + dag
        read_permissions = make_permissions(read, [dag])
        edit_permissions = make_permissions(edit, [dag])
        delete_permissions = make_permissions(delete, [dag])
    permissions += read_permissions + edit_permissions + delete_permissions

    data = {
        "actions": [*permissions],
        "name": new_role_name
    }

    airflow_url += "/api/roles"
    response = requests.post(airflow_url, json=data, headers=headers)

    if response.status_code == 403:
        raise PermissionError(f"Error 403 returned, please check if your AirFlow account is Op/Admin or verify the dags exist. \n {response.json()}")
    elif response.status_code == 401:
        raise PermissionError("Error 401 returned, please check the access token if the page is protected by an authentication")
    elif response.status_code == 200:
        print(f"Role `{new_role_name}` successfully created.")
    else:
        raise ConnectionError(f"An error occurred during role creation: {response.json()}")


def make_permissions(action, resources):
    permissions = []

    for perm in resources:
        permissions.append(make_permission(action, perm))

    return permissions


def make_permission(action, resource):

    return {
        "action": {"name": action},
        "resource": {"name": resource}
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--airflow-url", required=True, help="URL to the composer Airflow UI root page")
    parser.add_argument("-r", "--role-name", required=True, help="Name of the new created role")
    parser.add_argument("-d", "--dags", nargs="+", required=True, help="List of accessible dags for the role")

    args = parser.parse_args()
    create_rbac_role_with_permissions(
        args.airflow_url,
        args.role_name,
        args.dags,
    )
