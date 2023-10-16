SHELL = /bin/sh

#================================================================
# Usage
#================================================================
# make installations    # install the package for the first time, managing dependencies & performing a housekeeping cleanup too
# make deps     # just install the dependencies
# make install      # perform the end-to-end install
# make clean        # perform a housekeeping cleanup

#=======================================================================
# Variables
#=======================================================================
.EXPORT_ALL_VARIABLES:

# load variables from .env file
include .env

# load terminal colour formatting vars from separate file
include src/make/terminal_colour_formatting.mk

ASTRO_PROJECT_NAME := eg_astro_project
SNOWFLAKE_CONNECTION_NAME := dm_snowflake_conn
#=======================================================================

#=======================================================================
# Targets
#=======================================================================
all: clean deps install

deps:
	@echo && echo "${INFO}Called makefile target 'deps'. Create virtualenv with required Python libs.${COLOUR_OFF}" && echo
	@echo "Download Astro CLI"
	@curl -sSL install.astronomer.io | sudo bash -s > /dev/null 2>&1
	@pip install -r requirements.txt -q && echo

install: validate_env_vars
	@echo && echo "${INFO}Called makefile target 'install'. Set up GX (Great Expectations) project.${COLOUR_OFF}" && echo
	@echo "Step 1: Create an Astro project" && echo
	@mkdir ${ASTRO_PROJECT_NAME} && cd ${ASTRO_PROJECT_NAME} && astro dev init > /dev/null 2>&1
	@echo "Step 2: Generate template airflow_settings.yaml file"
	@j2 src/templates/jinja_templates/airflow_settings.yaml.j2 -o ${ASTRO_PROJECT_NAME}/airflow_settings.yaml
	@echo && echo "Step 3: Generate template Dockerfile" && echo
	@j2 src/templates/jinja_templates/Dockerfile.j2 -o ${ASTRO_PROJECT_NAME}/Dockerfile
	@echo "Step 4: Copy the generated .env file to the astro project dir" && echo
	@cp .env ${ASTRO_PROJECT_NAME}/.env
	@echo "Step 5: Copy over the template DAGs to the generated astro project dir" && echo
	@cp -r src/templates/template_dags/* ${ASTRO_PROJECT_NAME}/dags/
	@echo "Step 6: Remove the example dags" && echo
	@rm ${ASTRO_PROJECT_NAME}/dags/example_dag_basic.py && rm ${ASTRO_PROJECT_NAME}/dags/example_dag_advanced.py
	@echo "Step 7: Generate the template Makefile" && echo
	@j2 src/templates/jinja_templates/Makefile.j2 -o ${ASTRO_PROJECT_NAME}/Makefile && cp src/make/terminal_colour_formatting.mk ${ASTRO_PROJECT_NAME}

run:
	@echo && echo "${INFO}Called makefile target 'run'. Launch the service.${COLOUR_OFF}" && echo
	@echo "Run Airflow locally" && echo
	@cd ${ASTRO_PROJECT_NAME} && astro dev start

test:
	@echo && echo "${INFO}Called makefile target 'install'. Perform any required tests.${COLOUR_OFF}" && echo

validate_env_vars:
	@echo && echo "${INFO}Called makefile target 'validate_env_vars'. Verify the contents of required env vars.${COLOUR_OFF}" && echo
	@./src/sh/validate_env_vars.sh config.yaml .env

clean:
	@echo && echo "${INFO}Called makefile target 'clean'. Restoring the repository to its initial state.${COLOUR_OFF}" && echo
	@rm -rf ${ASTRO_PROJECT_NAME}

# Phony targets
.PHONY: all deps install test clean
# .PHONY tells Make that these targets don't represent files
# This prevents conflicts with any files named "all" or "clean"
