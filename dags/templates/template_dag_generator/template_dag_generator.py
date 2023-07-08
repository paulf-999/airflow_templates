#!/usr/bin/env python3
"""
Python Version  : 3.9
* Name          : template_dag_generator.py
* Description   : Demo jinja template script
* Created       : 07-07-2023
* Usage         : python3 template_dag_generator.py
"""

__author__ = "Paul Fry"
__version__ = "0.1"

import os
import logging
import shutil
import yaml
from jinja2 import Environment, FileSystemLoader

working_dir = os.getcwd()


"""Set up a specific logger with our desired output level"""
logging.basicConfig(format="%(message)s")
logger = logging.getLogger("application_logger")
logger.setLevel(logging.INFO)


def get_ips():
    """Read input from config file"""

    # store the credentials in a py dictionary
    af_template_ips = {}

    with open("config.yaml") as ip_yml:
        data = yaml.safe_load(ip_yml)

    af_template_ips["dag_name"] = data["general_params"]["dag_name"]
    af_template_ips["schedule_interval"] = data["general_params"]["schedule_interval"]
    af_template_ips["tags"] = data["general_params"]["tags"]
    af_template_ips["timezone"] = data["general_params"]["timezone"]
    af_template_ips["dagrun_timeout"] = data["general_params"]["dagrun_timeout"]

    logger.info(f"af_template_ips = {af_template_ips}")

    return af_template_ips


if __name__ == "__main__":
    """This is executed when run from the command line"""

    template_dir = os.path.join(working_dir, "templates")
    jinja_env = Environment(loader=FileSystemLoader(template_dir))
    template = jinja_env.get_template("airflow_dag.py.j2")

    af_template_ips = get_ips()

    # create a new folder for the path
    if not os.path.exists(os.path.join(working_dir, "op_dag", af_template_ips["dag_name"])):
        os.makedirs(os.path.join(working_dir, "op_dag", af_template_ips["dag_name"]))

    # copy over the template files
    shutil.copyfile(
        os.path.join(working_dir, "templates", "__dag_helpers.py"),
        os.path.join(working_dir, "op_dag", af_template_ips["dag_name"], "__dag_helpers.py"),
    )
    shutil.copyfile(
        os.path.join(working_dir, "templates", "__sql_queries.py"),
        os.path.join(working_dir, "op_dag", af_template_ips["dag_name"], "__sql_helpers.py"),
    )

    rendered_op = template.render(
        dag_name=af_template_ips["dag_name"],
        schedule_interval=af_template_ips["schedule_interval"],
        tags=af_template_ips["tags"],
        timezone=af_template_ips["timezone"],
        dagrun_timeout=af_template_ips["dagrun_timeout"],
    )

    with open(
        os.path.join(working_dir, "op_dag", af_template_ips["dag_name"], f"{af_template_ips['dag_name']}.py"),
        "w",
        encoding="UTF-8",
    ) as op:
        op.write(rendered_op)
