all: init_dbt_project setup_dbt_project_file validate_conn

export DBT_PROFILE_NAME=bikestores_cicd_demo
export DBT_PROJECT_NAME=bikestores
export DBT_MODEL=curated_db
export PROGRAM=DEMO

deps:
	$(info [+] Install dependencies (dbt))
	pip install --upgrade dbt
	brew install gettext
	brew link --force gettext
	brew install gnu-sed

init_dbt_project:
	$(info [+] Initialise dbt project)
	@echo
	###############################################################
	# call 'init_dbt_project'
	###############################################################
	@echo
	@[ "${DBT_PROJECT_NAME}" ] || ( echo "\nError: DBT_PROJECT_NAME variable is not set\n"; exit 1 )
	@[ "${DBT_PROFILE_NAME}" ] || ( echo "\nError: DBT_PROFILE_NAME variable is not set\n"; exit 1 )
	# populate profiles/profiles.yml with ${DBT_PROFILE_NAME} var
	@envsubst < templates/profiles.yml > profiles/profiles.yml
	@dbt init ${DBT_PROJECT_NAME} --profiles-dir=profiles 2>/dev/null
	# copy profiles and model dirs into project folder
	@cp -r profiles/ ${DBT_PROJECT_NAME}/profiles
	@cp -r models/ ${DBT_PROJECT_NAME}/models
	@cp -r tests/ ${DBT_PROJECT_NAME}/tests
	@cp -r macros/ ${DBT_PROJECT_NAME}/macros
	# copy schema.yml (data model tests) to project folder
	@cp schema.yml ${DBT_PROJECT_NAME}/models/
	@rm -r ${DBT_PROJECT_NAME}/models/example
	###############################################################
	# call 'setup_dbt_project_file'
	###############################################################
	@echo

setup_dbt_project_file:
	$(info [+] generate profiles.yml inside project folder file)
	@echo
	# change profile name in dbt_project.yml file
	@sed -i -e "s/profile: 'default'/profile: '${DBT_PROFILE_NAME}'/g" ${DBT_PROJECT_NAME}/dbt_project.yml
	# change project name in dbt_project.yml file
	@sed -i -e 's/my_new_project/${DBT_PROJECT_NAME}/g' ${DBT_PROJECT_NAME}/dbt_project.yml
	@rm ${DBT_PROJECT_NAME}/dbt_project.yml-e

validate_conn:
	$(info [+] Verify the connection to the source DB)
	cd ${DBT_PROJECT_NAME} && dbt debug --profiles-dir=profiles

run_model:
	$(info [+] Run the DBT model)
	cd ${DBT_PROJECT_NAME} && dbt run --profiles-dir profiles --models ${DBT_MODEL}

test_model:
	$(info [+] Test the DBT model. Note: this is a schema test only and is useful only for loading new data (enforces uniqueness))
	# prerequisite: populate ${DBT_PROJECT_NAME}/models/schema.yml with any desired tests
	cd ${DBT_PROJECT_NAME} && dbt test --profiles-dir profiles --models ${DBT_MODEL}

data_test_model:
	$(info [+] Test the DBT model. Note: this tests the actual data against predefined business rules)
	# prerequisite: populate ${DBT_PROJECT_NAME}/models/schema.yml with any desired tests
	cd ${DBT_PROJECT_NAME} && dbt test --data --profiles-dir profiles --models ${DBT_MODEL}

document_model:
	$(info [+] Document the DBT model)
	cd ${DBT_PROJECT_NAME} && dbt docs generate --profiles-dir profiles --models ${DBT_MODEL}
	cd ${DBT_PROJECT_NAME} && dbt docs serve --profiles-dir profiles

test_and_build:
	$(info [+] Test then if successful, build the DBT model)
	cd ${DBT_PROJECT_NAME} && dbt test --data --profiles-dir profiles --models ${DBT_MODEL}
	# following successful DBT tests, then run the DBT model
	cd ${DBT_PROJECT_NAME} && dbt run --profiles-dir profiles --models analytics_db
