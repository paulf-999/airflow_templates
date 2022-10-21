SHELL = /bin/sh

# note, you'll need to start the scheduler (using `make start_scheduler`) & webserver (using `make start_webserve`) in separate shells
all: installations init_airflow_db create_admin_user

CONFIG_FILE=envvars.json
########################################
# fetch inputs from config (json) file
########################################
# airflow args
installations: deps install clean

.PHONY: deps
deps:
	$(info [+] Download the relevant dependencies)
	# Airflow works a lot better with Python3.7 at the moment (compared to 3.8)
	# As such, set up your local Python version to use 3.7
	@brew install pyenv
	@brew install jq
	@pyenv install 3.7.10
	@pyenv local 3.7.10
	# note: ensure you add pyenv to your path file. Run `pyenv init` for instructions
	@pip install apache-airflow==${AIRFLOW_VERSION} --constraint ${CONSTRAINT_URL}

.PHONY: install
install:
	$(info [+] Install any required python / airflow libraries)
	@pip3 install wtforms==2.3.3
	@pip3 install SQLAlchemy==1.3.24

.PHONY: clean
clean:
	$(info [+] Remove any redundant files, e.g. downloads)

#############################################################################################
# Airflow-specific targets
#############################################################################################
# The two targets below are called by the above install target
init_airflow_db:
	$(info [+] Initialize the airflow db)
	@airflow initdb

create_admin_user:
	$(info [+] Create an admin user for Airflow)
	@airflow create_user \
		--username pfry \
		--firstname Peter \
		--lastname Parker \
		--role Admin \
		--email spiderman@superhero.org

# Note: you'll need to start the scheduler (using `make start_scheduler`) & webserver (using `make start_webserve`) in separate shells
start_scheduler:
	$(info [+] Start the scheduler)
	# open a new terminal or else run webserver with ``-D`` option to run it as a daemon
	@airflow scheduler

start_webserver:
	$(info [+] Start the web server, default port is 8080)
	@airflow webserver --port 8080
	# visit localhost:8080 in the browser and use the admin account just created to login

#############################################################################################
# Custom-Airflow targets
#############################################################################################
create_airflow_connections:
	$(info [+] Create some (example) Airflow connections)
	@airflow connections add slack_connection --conn-type http --conn-host https://hooks.slack.com/services --conn-password ${SLACK_TOKEN}

create_aws_connection:
	$(info [+] Create an Airflow AWS connection)
	@airflow connections add aws_conn --conn-type aws --conn-login ${AWS_ACCESS_KEY} --conn-password ${AWS_SECRET_ACCESS_KEY}

create_sf_connection:
	$(info [+] Create a Snowflake connection)
	#--account ${sf_acc_name_dbt_demo}
	#airflow connections add test --conn-type snowflake --conn-account ${sf_acc_name_dbt_demo} --conn-host localhost --conn-login ${sf_username_dbt_demo} --conn-password ${sf_pass_dbt_demo}
	airflow connections add snowflake_conn_eg --conn-type snowflake --conn-host 'sb83418.ap-southeast-2.snowflakecomputing.com' --conn-port 443 --conn-login ${sf_username_dbt_demo} --conn-password ${sf_pass_dbt_demo}
	#airflow connections add snowflake_conn_eg --conn-type snowflake --conn-host 'ocsp.snowflakecomputing.com:80' --conn-port 443 --conn-login ${sf_username_dbt_demo} --conn-password ${sf_pass_dbt_demo}

trigger_dag:
	$(info [+] Trigger an Airflow DAG)
	@airflow dags trigger dbt_dag

trigger_dag_w_ip:
	$(info [+] Trigger an Airflow DAG with input provided)
	@airflow dags trigger template_dms_task_dag --conf '{"dms_task_name":"example-task"}'

debug:
	# use this if you need to reinstall airflow
	rm ~/airflow/airflow.db
