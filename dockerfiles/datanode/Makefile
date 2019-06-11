
DOCKER_IMAGE_VERSION := "ownport/datastax-datanode:6.7.3-v1" 

build:
	docker build --tag ${DOCKER_IMAGE_VERSION} .

console:
	@ docker run -ti --rm --name datastax-datanode-console \
		--entrypoint "bash" ${DOCKER_IMAGE_VERSION} 

