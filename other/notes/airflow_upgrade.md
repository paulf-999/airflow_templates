# Airflow upgrade

## Pre-reqs
- python 3.6+
- backport availability with 1.10.15(bridge release)

## DAG Upgrade check
- pachakge apache-airflow-upgrade-check helps identifu dags
- works with 1.10.14 or 1.101.15
- verifies incompatible changes on airflow.cfg, DAG files, plugins, airflow connections

## Commands
``` python
pip install apache-airflow["$AIRFLOW_COMPONENT"]==1.10.15 --constraint requirements-python3.6.txt --upgrade

pip install apache-airflow-upgrade-check

airflow upgrade_check
```

## Config Changes
- [scheduler] max_threads -> [scheduler] parsing_processes
- grouping changes - logging config is moved from core to ligging, metric config moved from scheduler to metrics
-new ui with rbac is recommended
```
[webserver]
rbac = True
```

## Connection
- Duplicate connectin ids are not allowed
- Connection types are only visible for "installed providers"(providers installed via pip)

## Upgrade steps
- Turn of all the dags and ensure no task is running
- backup metadata db and config files
- stop webserver, schedlurer and workers
- upgrade to the 2.x version and use --constraint feature
- install all the required providers using "extras"
- upgrae the database `airflow db upgrade`

## Sources
- https://airflow.apache.org/docs/apache-airflow/stable/upgrading-from-1-10/index.html
