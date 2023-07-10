all: deps install [X, Y, Z...] clean

.EXPORT_ALL_VARIABLES:

.PHONY = installations deps install get_ips build_docker_img deploy_image_to_artifactory run_docker_container_locally

CONFIG_FILE := config.json

installations: deps install clean

deps:
	$(info [+] Download the relevant dependencies)
	pip3 install jq -q
	# install the jfrog cli tool
	brew install jfrog-cli && jf intro

install:
	$(info [+] Install the relevant dependencies)
	@make -s build_docker_img
	@make -s deploy_image_to_artifactory

get_ips:
	@# Target: 'get_ips'. Get input args from config.json
	$(eval ENV=$(shell jq -r '.SharedParameters.Env' ${CONFIG_FILE}))
	$(eval ARTIFACTORY_REGISTRY=$(shell jq -r '.ArtifactoryParameters.ArtifactoryRegistry' ${CONFIG_FILE}))
	$(eval ARTIFACTORY_REPO=$(shell jq -r '.ArtifactoryParameters.ArtifactoryRepo' ${CONFIG_FILE}))
	$(eval DOCKER_IMAGE_NAME=$(shell jq -r '.ArtifactoryParameters.DockerImageName' ${CONFIG_FILE}))
	$(eval ARTIFACTORY_IMAGE_PATH=$(shell jq -r '.ArtifactoryParameters.ArtifactoryImagePath' ${CONFIG_FILE}))
	$(eval USERNAME=$(shell jq -r '.ArtifactoryCredentials.Username' ${CONFIG_FILE}))
	$(eval PWD=$(shell jq -r '.ArtifactoryCredentials.Pwd' ${CONFIG_FILE}))

	@# debugging
	@#@echo "env = ${ENV}"
	@#@echo "ARTIFACTORY_REGISTRY = ${ARTIFACTORY_REGISTRY}"
	@#@echo "ARTIFACTORY_REPO = ${ARTIFACTORY_REPO}"
	@#@echo "DOCKER_IMAGE_NAME = ${DOCKER_IMAGE_NAME}"
	@#@echo "ARTIFACTORY_IMAGE_PATH = ${ARTIFACTORY_IMAGE_PATH}"
	@#@echo "USERNAME = ${USERNAME}"
	@#@echo "PWD" = ${PWD}

build_docker_img: get_ips
	$(info [+] Target: 'build_docker_img'. (Locally) build the Docker image. See `Dockerfile` for further details)
	@echo
	docker build -f Dockerfile -t ${ARTIFACTORY_IMAGE_PATH} .
	@echo

deploy_image_to_artifactory: get_ips
	$(info [+] Target: 'deploy_image_to_artifactory'. Push the locally built Docker image to Artifactory)
	jfrog rt docker-push \
		${ARTIFACTORY_IMAGE_PATH} \
		${DOCKER_IMAGE_NAME} \
		--project "${DOCKER_IMAGE_NAME}" \
		--url "https://${ARTIFACTORY_REGISTRY}/artifactory" \
		--user ${USERNAME} \
		--password ${PWD}

# NOTE: this target is only used for debugging purposes (i.e., running the image locally before deploying to Artifactory)
run_docker_container_locally: get_ips
	docker run -it ${ARTIFACTORY_IMAGE_PATH} standalone

ssh_onto_image:
	# change the image ID below
	#docker exec -it <image id> /bin/bash
	docker exec -it 2aec796d849c /bin/bash
