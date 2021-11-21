SHELL = /bin/sh

# note, you'll need to start the scheduler (using 'make start_scheduler') in a separate shell
all: installations init_airflow_db create_admin_user

config_file=envvars.json
########################################
# fetch inputs from config (json) file
########################################
# airflow args
$(eval AIRFLOW_VERSION=$(shell jq '.airflow_args.airflow_version' ${config_file}))
$(eval PYTHON_VERSION=$(shell jq '.airflow_args.python_version' ${config_file}))
$(eval CONSTRAINT_URL=$(shell jq '.airflow_args.constraints_url' ${config_file}))
$(eval AIRFLOW_HOME_DIR=$(shell jq '.other.airflow_home_dir' ${config_file}))
# sample db cred args
$(eval HOST=$(shell jq '.sample_db_creds.host' ${config_file}))
$(eval USERNAME=$(shell jq '.sample_db_creds.username' ${config_file}))
$(eval PWD=$(shell jq '.sample_db_creds.password' ${config_file}))
$(eval DB_NAME=$(shell jq '.sample_db_creds.db_name' ${config_file}))
$(eval DB_SCHEMA=$(shell jq '.sample_db_creds.db_schema' ${config_file}))
$(eval IP_TBLS=$(shell jq '.sample_db_creds.ip_tbl_list' ${config_file}))
# other
$(eval SLACK_TOKEN=$(shell jq '.other.slack_token' ${config_file}))

installations: deps install clean

.PHONY: deps
deps:
	$(info [+] Download the relevant dependencies)
	# airflow works a lot better with Python3.7 at the moment (compared to 3.8)
	# as such, set up your local Python version to use 3.7
	@brew install pyenv
	@pyenv install 3.7.10
	@pyenv local 3.7.10
	@pip install airflow-dbt
	@pip install snowflake-connector-python
	@pip install snowflake-sqlalchemy
	@brew install jq
	# note: ensure you add pyenv to your path file. Run `pyenv init` for instructions

.PHONY: install
install:
	$(info [+] Install any required python / airflow libraries)
	@pip install apache-airflow==${AIRFLOW_VERSION} --constraint ${CONSTRAINT_URL}
	@pip install apache-airflow-providers-amazon --constraint "${CONSTRAINT_URL}"
	@pip install apache-airflow-providers-slack --constraint "${CONSTRAINT_URL}"
	# the 2 below are for any db-related operations
	@#pip install apache-airflow-providers-odbc --constraint "${CONSTRAINT_URL}"
	@#pip install apache-airflow-providers-microsoft-mssql --constraint "${CONSTRAINT_URL}"
	@#pip install apache-airflow-providers-snowflake --constraint "${CONSTRAINT_URL}"
	@pip install snowflake-connector-python
	@pip install snowflake-sqlalchemy
	# call routine to create the admin user
	@make create_admin_user
	# copy over additional config to be used to capture task runtime stats
	# first you need to remove the quotes from the var
	@$(eval AIRFLOW_HOME_DIR := $(subst $\",,$(AIRFLOW_HOME_DIR)))
	@cp notes/airflow_local_settings.py ${AIRFLOW_HOME_DIR}config/

.PHONY: clean
clean:
	$(info [+] Remove any redundant files, e.g. downloads)

init_airflow_db:
	$(info [+] Initialize the airflow db)
	@airflow db init

create_admin_user:
	$(info [+] Create an admin user for Airflow)
	@airflow users create \
		--username pfry \
		--firstname Peter \
		--lastname Parker \
		--role Admin \
		--email spiderman@superhero.org

start_webserver:
	$(info [+] Start the web server, default port is 8080)
	@airflow webserver --port 8080

start_scheduler:
	$(info [+] Start the scheduler)
	# open a new terminal or else run webserver with ``-D`` option to run it as a daemon
	@airflow scheduler
	# visit localhost:8080 in the browser and use the admin account just created to login

create_airflow_variables:
	$(info [+] Create some (example) Airflow variables)
	@airflow variables set host ${HOST}
	@airflow variables set username ${USERNAME}
	@airflow variables set password ${PWD}
	@airflow variables set db_name ${DB_NAME}
	@airflow variables set db_schema ${DB_SCHEMA}
	@airflow variables set ip_tbl_list ${IP_TBLS}
	@airflow variables set slack_token ${SLACK_TOKEN}
	@airflow variables set AWS_ACCESS_KEY ${AWS_ACCESS_KEY}
	@airflow variables set AWS_SECRET_ACCESS_KEY ${AWS_SECRET_ACCESS_KEY}

create_airflow_connections:
	$(info [+] Create some (example) Airflow connections)
	@airflow connections add slack_connection --conn-type http --conn-host https://hooks.slack.com/services --conn-password ${SLACK_TOKEN}

create_aws_connection:
	$(info [+] Create an Airflow AWS connection)
	@airflow connections add aws_conn --conn-type aws --conn-login ${AWS_ACCESS_KEY} --conn-password ${AWS_SECRET_ACCESS_KEY}

create_sf_connection:
	$(info [+] Create a Snowflake connection)
	#--account ${sf_acc_name_dbt_demo}
	#airflow connections add snowflake_conn_eg --conn-type snowflake --conn-account ${sf_acc_name_dbt_demo} --conn-host localhost --conn-login ${sf_username_dbt_demo} --conn-password ${sf_pass_dbt_demo}
	airflow connections add test --conn-type snowflake --conn-host 'sb83418.ap-southeast-2.snowflakecomputing.com' --conn-port 443 --conn-login ${sf_username_dbt_demo} --conn-password ${sf_pass_dbt_demo}

trigger_dag:
	$(info [+] Trigger an Airflow DAG)
	@airflow dags trigger dbt_dag

trigger_dag_w_ip:
	$(info [+] Trigger an Airflow DAG with input provided)
	@airflow dags trigger template_dms_task_dag --conf '{"dms_task_name":"example-task"}'
