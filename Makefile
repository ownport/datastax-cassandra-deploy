
pull-datastax-opscenter:
	@ docker pull datastax/dse-opscenter:6.7.3

pull-datastax-server:
	@ docker pull datastax/dse-server:6.7.3

.PHONY: test
test:
	@ drone exec --event=run-tests

.PHONY: deploy-test-cluster
deploy-test-cluster-console:
	@ docker container run -ti --rm --name deploy-test-cluster-console \
		-v $(shell pwd):/deploy \
		--network resources_default \
		ownport/datastax-cassandra-test-evn:0.1.0 \
		sh -c 'cd /deploy && pip3 install -e . && \
				ds-cas-deploy \
					-d test/resources/configs/test-env/opscenter.yaml \
					-d test/resources/configs/test-env/credentials.yaml \
					-d test/resources/configs/test-env/config-profiles.yaml \
					-d test/resources/configs/test-env/repositories.yaml \
					-d test/resources/configs/test-env/test-cluster.yaml'

.PHONY: ds-cas-deploy-console
ds-cas-deploy-console:
	@ docker container run -ti --rm --name ds-cas-deploy-console \
		-v $(shell pwd):/deploy \
		ownport/datastax-cassandra-test-evn:0.1.0 \
		sh -c 'cd /deploy && pip3 install -e . && \
				ds-cas-deploy --help'

