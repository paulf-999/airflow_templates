SHELL = /bin/sh

# Load environment variables from .env file
include .env

# load variables from a separate file
include src/make/variables.mk

#=======================================================================
# Targets
#=======================================================================
gen_env_template:
	@echo && echo "Generate the template .env file"
	@j2 src/jinja_templates/.env_template.j2 -o .env

install:
	@echo && echo "${INFO}Called makefile target 'install'. Run the setup & install targs.${COLOUR_OFF}" && echo
	@echo && echo "Step 1: Create an Astro project" && echo
	@mkdir ${ASTRO_PROJECT_NAME} && cd ${ASTRO_PROJECT_NAME} && astro dev init > /dev/null 2>&1 && touch tests/.gitkeep
	@echo "Step 2: Generate template airflow_settings.yaml file"
	@j2 src/templates/jinja_templates/airflow_settings.yaml.j2 -o ${ASTRO_PROJECT_NAME}/airflow_settings.yaml
	@echo && echo "Step 3: Generate template Dockerfile" && echo
	@j2 src/templates/jinja_templates/Dockerfile.j2 -o ${ASTRO_PROJECT_NAME}/Dockerfile
	@echo "Step 4: Copy the generated .env file to the astro project dir" && echo
	@cp .env ${ASTRO_PROJECT_NAME}/.env
	@echo "Step 5: Copy over the template DAGs to the generated astro project dir" && echo
	@cp -r src/templates/template_dags/* ${ASTRO_PROJECT_NAME}/dags/
	@echo "Step 6: Copy the template soda config to the astro project dir" && echo
	@cp -r src/templates/soda/ ${ASTRO_PROJECT_NAME}/include/
	@echo "Step 7: Remove the example dags" && echo
	@rm ${ASTRO_PROJECT_NAME}/dags/example_dag_basic.py && rm ${ASTRO_PROJECT_NAME}/dags/example_dag_advanced.py
	@echo "Step 8: Generate the template Makefile" && echo
	@j2 src/templates/jinja_templates/Makefile.j2 -o ${ASTRO_PROJECT_NAME}/Makefile && cp config.mk ${ASTRO_PROJECT_NAME}

# Phony targets
.PHONY: gen_env_template create_svc_cicd_user_and_role get_ips
# .PHONY tells Make that these targets don't represent files
# This prevents conflicts with any files named "all" or "clean"
