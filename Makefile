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

# setup colour formatting
RED := \033[0;31m
YELLOW := \033[0;33m
GREEN := \033[0;32m
PURPLE := \033[0;35m
CYAN := \033[0;36m
COLOUR_OFF := \033[0m # Text Reset

ASTRO_PROJECT_NAME := eg_astro_project

#=======================================================================

.PHONY = installations deps install clean

installations: deps install clean

deps:
    @echo "----------------------------------------------------------------------------------------------------------------------"
    @echo "${YELLOW}Target: 'deps'. Download the relevant pip package dependencies (note: ignore the pip depedency resolver errors.)${COLOUR_OFF}"
    @echo "----------------------------------------------------------------------------------------------------------------------"
    @echo && echo "Download astro cli" && echo
    @curl -sSL install.astronomer.io | sudo bash -s > /dev/null 2>&1

install:
    @echo "------------------------------------------------------------------"
    @echo "${YELLOW}Target: 'install'. Run the setup and install targets.${COLOUR_OFF}"
    @echo "------------------------------------------------------------------"
    @echo && echo "Step 1: Create an Astro project" && echo
    @mkdir ${ASTRO_PROJECT_NAME} && cd ${ASTRO_PROJECT_NAME} && astro dev init > /dev/null 2>&1
    @echo "Step 2: Run Airflow locally" && echo
    @cd ${ASTRO_PROJECT_NAME} && astro dev start

clean:
    @echo "------------------------------------------------------------------"
    @echo "${YELLOW}Target 'clean'. Remove any redundant files, e.g. downloads.${COLOUR_OFF}"
    @echo "------------------------------------------------------------------"
    @rm -rf ${ASTRO_PROJECT_NAME}
