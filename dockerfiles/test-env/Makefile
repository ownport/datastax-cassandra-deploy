
DOCKER_IMAGE_VERSION := "ownport/datastax-cassandra-test-evn:0.1.0" 

build:
	docker build --tag ${DOCKER_IMAGE_VERSION} .

console:
	@ docker run -ti --rm --name datastax-cassandra-test-env-console \
		${DOCKER_IMAGE_VERSION} \
		bash

