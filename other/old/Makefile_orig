SHELL = /bin/sh

all: installations

export adm_pass=${sf_pass_dbt_demo}
export user_demo_pass=${user_demo}

CONFIG_FILE=ip/config.json
PIP_INSTALL_CMD=pip3 install -q --disable-pip-version-check
########################################
# fetch inputs from config (json) file
########################################
# airflow args
$(eval AIRFLOW_VERSION=$(shell jq '.airflow_args.airflow_version' ${CONFIG_FILE}))
$(eval PYTHON_VERSION=$(shell jq '.airflow_args.python_version' ${CONFIG_FILE}))
$(eval CONSTRAINT_URL=$(shell jq '.airflow_args.constraints_url' ${CONFIG_FILE}))
$(eval AIRFLOW_HOME_DIR=$(shell jq '.airflow_args.airflow_home_dir' ${CONFIG_FILE}))

installations: deps install clean

.PHONY: deps
deps:
	$(info [+] Download the relevant dependencies)
	@${PIP_INSTALL_CMD} jq
	@${PIP_INSTALL_CMD} apache-airflow==${AIRFLOW_VERSION}
	@${PIP_INSTALL_CMD} -r requirements.txt

.PHONY: install
install:
	$(info [+] Install any required python / airflow libraries)
	# Initialize the airflow db
	@airflow db init
	@sleep 10
	# copy over the predefined airflow config
	@cp ip/airflow.cfg	$(subst $\",,$(AIRFLOW_HOME_DIR))
	# Create the admin user
	@make create_admin_user
	# create example 'read-only' and 'creator' users
	@make create_ro_user_example
	@make create_creator_user_example
	# start the airflow scheduler & webserver
	# open a new terminal or else run webserver with ``-D`` option to run it as a daemon
	@airflow scheduler -D
	@airflow webserver --port 8080 -D
	# visit localhost:8080 in the browser and use the admin account just created to login

.PHONY: clean
clean:
	$(info [+] Remove any redundant files, e.g. downloads)

#############################################################################################
# Airflow-specific targets
#############################################################################################
# The two targets below are called by the above install target

create_admin_user:
	$(info [+] Create an admin user for Airflow)
	@airflow users create \
		--username pfry \
		--password ${adm_pass} \
		--firstname Peter \
		--lastname Parker \
		--role Admin \
		--email spiderman@superhero.org

create_ro_user_example:
	$(info [+] Create user & assign them the 'user' role in Airflow)
	@airflow users create \
		--username read_only_demo \
		--password ${user_demo_pass} \
		--firstname read_only_demo \
		--lastname read_only_demo \
		--role Viewer \
		--email read_only_demo@test.com

create_creator_user_example:
	$(info [+] Create user & assign them the 'user' role in Airflow)
	@airflow users create \
		--username creator_demo \
		--password ${user_demo_pass} \
		--firstname creator_demo \
		--lastname creator_demo \
		--role User \
		--email creator_demo@test.com

create_custom_role_example:
	curl -X POST http://localhost:8080/api/v1/roles \
	-H "Content-Type: application/json" \
	--user "pfry:${adm_pass}" \
	-d "{\"name\":\"read_only_role\", \"actions\":[{\"action\":{\"name\":\"can_read\"},\"resource\":{\"name\":\"DAGs\"}}]}"

add_user_to_role:
	airflow users add-role -u pfry -r read_only_role

#############################################################################################
# Custom-Airflow targets
#############################################################################################
trigger_dag:
	$(info [+] Trigger an Airflow DAG)
	@airflow dags trigger dbt_dag

trigger_dag_w_ip:
	$(info [+] Trigger an Airflow DAG with input provided)
	@airflow dags trigger template_dms_task_dag --conf '{"dms_task_name":"example-task"}'

#############################################################################################
# Airflow tests
#############################################################################################
test:
	pytest tests/test_dag_loader.py --dag_name example_dag --disable-pytest-warnings -v -q

test2:
	pytest tests/test_dag_validation.py --dag_name example_dag --disable-pytest-warnings -v -q

#############################################################################################
# Drop Airflow instance
#############################################################################################
debug:
	# use this if you need to reinstall airflow
	@ rm -r ~/airflow/
	@ rm ~/airflow/airflow.db

kill_af_scheduler_and_webserver:
	# stop the Airflow scheduler & webserver
	@cat ~/airflow/airflow-scheduler.pid | xargs kill
	@cat ~/airflow/airflow-webserver.pid | xargs kill

#############################################################################################
# Docker
#############################################################################################
docker:
	#docker run apache/airflow:2.0.2-python3.7
	#docker-compose start
	#docker pull apache/airflow:2.0.2-python3.7
	docker build --pull -t apache/airflow:2.0.2-python3.7 .

logging:
	airflow db init 2>null
