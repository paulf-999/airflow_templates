## Template dbt DAG

**Description**:    Reusable/cookie-cutter DAG for developing Airflow-DBT DAGs on the local AF2 instance

**Date Created**:   26-07-2022

**Notes**: To do development of Airflow DAGs (that invoke DBT) locally, you need to do the following:

1) Copy your DBT project into the `dbt` folder at the root of the DAGs repo. I.e.:

```
    dags/
    dbt/ <- in here
    docs/
    modules/
    tests/
```

2) Within your DAG, update the value of the variable `dbt_project_dir` to the path of the DBT project. E.g.:

`dbt_project_dir = "/opt/airflow/dags/dbt/dbt_ofw"`

3) Copy your Snowflake private key into the DBT `/profiles` folder & save it as `snowflake-rsa-key.p8`

4) Update the user listed profiles.yml file, to instead use your own credentials. E.g.:

The arg for user (below) needs to reflect your Snowflake username:

```
    dbt_svc_profile:
    target: dev
    outputs:
        dev:
        type: snowflake
        account:
        role:

        user:
        private_key_path:

        database:
        warehouse:
        schema:
        threads:
```
