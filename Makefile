all: install_airflow init_airflow_db create_admin_user

CONFIG_FILE=ip/config.json
########################################
# fetch inputs from config (json) file
########################################
# airflow args
$(eval AIRFLOW_VERSION=$(shell jq '.airflow_args.airflow_version' ${CONFIG_FILE}))
$(eval PYTHON_VERSION=$(shell jq '.airflow_args.python_version' ${CONFIG_FILE}))
$(eval CONSTRAINT_URL=$(shell jq '.airflow_args.constraints_url' ${CONFIG_FILE}))
# sample db cred args
$(eval HOST=$(shell jq '.sample_db_creds.host' ${CONFIG_FILE}))
$(eval USERNAME=$(shell jq '.sample_db_creds.username' ${CONFIG_FILE}))
$(eval PWD=$(shell jq '.sample_db_creds.password' ${CONFIG_FILE}))
$(eval DB_NAME=$(shell jq '.sample_db_creds.db_name' ${CONFIG_FILE}))
$(eval DB_SCHEMA=$(shell jq '.sample_db_creds.db_schema' ${CONFIG_FILE}))
$(eval IP_TBLS=$(shell jq '.sample_db_creds.ip_tbl_list' ${CONFIG_FILE}))
# other
$(eval SLACK_TOKEN=$(shell jq '.other.slack_token' ${CONFIG_FILE}))

deps:
	pip3 install airflow-dbt
	brew install jq
	# airflow works a lot better with Python3.7 at the moment (compared to 3.8)
	# as such, set up your local Python version to use 3.7
	brew install pyenv
	pyenv install 3.7.10
	pyenv local 3.7.10
	# note: ensure you add pyenv to your path file. Run `pyenv init` for instructions

install_airflow:
	$(info [+] Install any required python / airflow libraries)
	pip install apache-airflow==${AIRFLOW_VERSION} --constraint ${CONSTRAINT_URL}
	pip install apache-airflow-providers-amazon --constraint "${CONSTRAINT_URL}"
	pip install apache-airflow-providers-slack --constraint "${CONSTRAINT_URL}"
	# the 2 below are for any db-related operations
	#pip install apache-airflow-providers-odbc --constraint "${CONSTRAINT_URL}"
	#pip install apache-airflow-providers-microsoft-mssql --constraint "${CONSTRAINT_URL}"

init_airflow_db:
	$(info [+] Initialize the airflow db)
	airflow db init

create_admin_user:
	$(info [+] Create an admin user for Airflow)
	airflow users create \
		--username pfry \
		--firstname Peter \
		--lastname Parker \
		--role Admin \
		--email spiderman@superhero.org

start_webserver:
	$(info [+] Start the web server, default port is 8080)
	airflow webserver --port 8080

start_scheduler:
	$(info [+] Start the scheduler)
	# open a new terminal or else run webserver with ``-D`` option to run it as a daemon
	airflow scheduler

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
	airflow connections add slack_connection --conn-type http --conn-host https://hooks.slack.com/services --conn-password ${SLACK_TOKEN}

create_aws_connection:
	$(info [+] Create an Airflow AWS connection)
	airflow connections add aws_conn --conn-type aws --conn-login ${AWS_ACCESS_KEY} --conn-password ${AWS_SECRET_ACCESS_KEY}

trigger_dag:
	$(info [+] Trigger an Airflow DAG)
	airflow dags trigger dbt_dag

trigger_dag_w_ip:
	$(info [+] Trigger an Airflow DAG with input provided)
	airflow dags trigger template_dms_task_dag --conf '{"dms_task_name":"example-task"}'

airflow_dbt:
	$(info [+] Make use of the Python package, 'airflow-dbt'. Note: there is a prerequisite Python package, listed in `deps`)
