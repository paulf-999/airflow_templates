#!/bin/bash
#================================================================
## HEADER
#================================================================
## Overview:    Git branch validation.
##
## Description: This script is used within a Git CICD job and
##              is used to verify the user's git branch name
##              follows the naming standard:
##              ^(feature|hotfix|release)\/[a-z0-9_]+$
##
## Usage: ./validate_git_branch_name.sh <input git branch name>
##
#================================================================

#=======================================================================
# Variables
#=======================================================================

# determine the name of the local git branch name
LOCAL_GIT_BRANCH_NAME="$(git rev-parse --abbrev-ref HEAD)"
# the regex for valid git branch names
VALID_GIT_BRANCH_NAME="^(feature|hotfix|release)\/[a-z0-9_]+$"

# setup colour formatting
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
COLOUR_OFF='\033[0m' # Text Reset

#=======================================================================
# Main script logic
#=======================================================================

# Validate the Git branch name used
if [[ ! $LOCAL_GIT_BRANCH_NAME =~ $VALID_GIT_BRANCH_NAME ]]
then
    echo
    echo -e "${RED}#############################################################################################"
    echo -e "${RED}# ERROR: Invalid Git branch name."
    echo -e "${RED}#############################################################################################${COLOUR_OFF}"
    echo -e "Local git branch name = $LOCAL_GIT_BRANCH_NAME"
    echo
    echo -e "Git branch name needs to adhere to the following regex: $VALID_GIT_BRANCH_NAME."
    echo
    echo -e "I.e., it needs to:"
    echo
    echo -e "* Start with either 'feature/', 'hotfix/' or 'release/'"
    echo -e "* Followed by a snake_case description of your change (note, hyphens aren't allowed)."
    echo
    echo -e "E.g.: feature/my_eg_change"
    echo
    exit 1
else
    echo -e "${GREEN}#############################################################################################"
    echo -e "${GREEN}# SUCCESS: Valid Git branch name"
    echo -e "${GREEN}#############################################################################################${COLOUR_OFF}"
    echo
fi
