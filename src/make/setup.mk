SHELL = /bin/sh

include .env # load environment variables from .env file
include src/make/variables.mk # load variables from a separate file

#=======================================================================
# Targets
#=======================================================================
gen_env_template:
	@echo "${DEBUG}2. Generate template .env file${COLOUR_OFF}"
	@j2 ${JINJA_TEMPLATES_DIR}/.env_template.j2 -o .env && echo

create_astro_project:
	@echo "${DEBUG}1: Create an Astro project${COLOUR_OFF}"
	@make -s prompt_remove_directory
	@mkdir ${ASTRO_PROJECT_NAME}
	@cd ${ASTRO_PROJECT_NAME} && astro dev init > /dev/null 2>&1 && touch tests/.gitkeep

prompt_remove_directory:
	@if [ -d "${ASTRO_PROJECT_NAME}" ]; then \
		printf "\nThe target directory '${ASTRO_PROJECT_NAME}' already exists. Do you want to remove it? (y/n): "; \
		read answer; \
		if [ "$$answer" != "y" ]; then \
			printf "${ERROR}\nInstallation aborted - Astronomer project directory already exists.\n${COLOUR_OFF}"; \
			exit 1; \
		else \
			rm -rf "${ASTRO_PROJECT_NAME}" && echo; \
		fi; \
	fi

copy_generated_airflow_files:
	@echo "${DEBUG}2. Copy generated Airflow files into Astronomer project.${COLOUR_OFF}"
	@# Copy the generated .env file to the astro project dir
	@cp .env ${ASTRO_PROJECT_NAME}/.env
	@# Copy over the template DAGs to the generated astro project dir
	@cp -r dags/templates/ ${AIRFLOW_DAGS_DIR}/
	@# Copy the template soda config to the astro project dir
	@cp -r ${TEMPLATES_DIR}/soda/ ${ASTRO_PROJECT_NAME}/include/
	@# Remove the example dags
	@rm ${AIRFLOW_DAGS_DIR}/example_dag_basic.py && rm ${AIRFLOW_DAGS_DIR}/example_dag_advanced.py && echo

generate_airflow_project_files:
	@echo "${DEBUG}3. Generate Airflow files.${COLOUR_OFF}" && echo
	@# Generate template airflow_settings.yaml file
	@j2 ${JINJA_TEMPLATES_DIR}/airflow_settings.yaml.j2 -o ${ASTRO_PROJECT_NAME}/airflow_settings.yaml
	@# Generate template Dockerfile
	@j2 ${JINJA_TEMPLATES_DIR}/Dockerfile.j2 -o ${ASTRO_PROJECT_NAME}/Dockerfile
	@# Generate the template Makefile
	@j2 ${JINJA_TEMPLATES_DIR}/Makefile.j2 -o ${ASTRO_PROJECT_NAME}/Makefile
	@mkdir ${ASTRO_PROJECT_NAME}/src && mkdir ${ASTRO_PROJECT_NAME}/src/make && cp src/make/variables.mk ${ASTRO_PROJECT_NAME}

check_docker:
	@echo "${DEBUG}Check if Docker is running before proceeding.${COLOUR_OFF}"
	@if [ "$$(docker info --format '{{.ServerVersion}}' 2>/dev/null)" = "" ]; then \
		echo "${ERROR}Error: Docker is not running. Please launch Docker and try launching Astronomer again.${COLOUR_OFF}"; \
		exit 1; \
	else \
		echo "${DEBUG}Docker is running.${COLOUR_OFF}"; \
	fi

validate_env_vars:
	@echo && echo "${INFO}Called makefile target 'validate_env_vars'. Verify the contents of required env vars.${COLOUR_OFF}" && echo
	@./src/sh/validate_env_vars.sh config.yaml .env

# Phony targets
.PHONY: gen_env_template create_astro_project prompt_remove_directory generate_airflow_project_files copy_generated_airflow_files check_docker
# .PHONY tells Make that these targets don't represent files
# This prevents conflicts with any files named "all" or "clean"
