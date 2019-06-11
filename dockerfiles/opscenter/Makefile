
DOCKER_IMAGE_VERSION := "ownport/datastax-opscenter:6.7.3-v1" 

build:
	docker build --tag ${DOCKER_IMAGE_VERSION} .


run-opscenter-in-console:
	@ docker run -ti --rm --name datastax-opscenter-console \
		${DOCKER_IMAGE_VERSION}

console:
	@ docker run -ti --rm --name datastax-opscenter-console \
		--entrypoint "bash" ${DOCKER_IMAGE_VERSION} 

