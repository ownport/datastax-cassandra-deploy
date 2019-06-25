# Datastax Cassandra Deployment

The main idea of this project is apply Infrasrtucture As Code approach for DataStax Cassandra. Inspired by:
- [DSPN/install-datastax-ubuntu](https://github.com/DSPN/install-datastax-ubuntu) bash scripts to install and configure DataStax Enterprise (DSE) and OpsCenter on Ubuntu 
- [oracle/oci-quickstart-datastax](https://github.com/oracle/oci-quickstart-datastax) Terraform module to deploy DataStax Enterprise (DSE) on Oracle Cloud Infrastructure (OCI) 

## Disclaimer

The software is under development and not finalized yet. The use of this repo is intended for development purpose only. Usage of this repo is solely at user’s own risks. 

## Licence

These scripts use DataStax Enterprise.  By using these scripts the user accepts the licensing terms set forth here: http://www.datastax.com/enterprise-terms

## How to install

```sh
pip3 install git+https://github.com/ownport/datastax-cassandra-deploy
```

## How to use
```sh
ds-cas-deploy --help

usage: ds-cas-deploy [-h] [-v] [-l LOG_LEVEL] [-a ACTION] [-s SECTION]
                     [-o OUTPUT] [-d DEPLOYMENT]

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -l LOG_LEVEL, --log-level LOG_LEVEL
                        Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL
  -a ACTION, --action ACTION
                        Actions: deploy | dump
  -s SECTION, --section SECTION
                        The section for config dump. Possible values:
                        credentials, config-profiles, datacenters,
                        repositories, clusters
  -o OUTPUT, --output OUTPUT
                        The output path for config dump, JSON file
  -d DEPLOYMENT, --deployment DEPLOYMENT
                        the path to deployment configuration. Support
                        YAML/JSON file
```

To run deployment
```sh
ds-cas-deploy \
  --action deploy \
	--deployment test/resources/configs/test-env/opscenter.yaml \
	--deployment test/resources/configs/test-env/credentials.yaml \
	--deployment test/resources/configs/test-env/config-profiles.yaml \
	--deployment test/resources/configs/test-env/repositories.yaml \
  --deployment test/resources/configs/test-env/test-cluster.yaml
```

To dump data from OpsCenter
```sh
ds-cas-deploy \
  --action dump \
  --section credentials \
  --section config-profiles \
  --section datacenters \
  --section repositories \
  --output test/resources/configs/test-env/opscenter-dump.json \
	--deployment test/resources/configs/test-env/opscenter.yaml
```


## Deployment configs (sample)

Only opscenter section is mandatory. It is required for connection to DataStax OpsCenter. The rest sections are optional:
- credentials
- repositories
- config-profiles
- datacenters
- clusters

For instance, if credentials, repositories or config profiles were created before there are no need to specify them again 

opscenter.yaml
```yaml
opscenter:
  hostname: 172.19.0.3
  username: admin
  password: admin
  timeout: 25
  attempts: 3
```

credentials.yaml
```yaml
credentials:
- name: test-ssh-creds
  become-mode: sudo
  use-ssh-keys: true
  login-user: cassandra
  login-password:  null
  ssh-private-key: test/resources/keys/cassandra
  ssh-unlock:  null
  become-user: null
  become-password: null
```

repositories.yaml
```yaml
repositories:
- name: test-repository
  repo-key-url: null
  repo-url: null
  username: test
  password: test
  use-proxy: false
  deb-dist: null
  deb-components: null,
  manual-repository-setup: true
  comment: Test DataStax Repository
```

config-profiles.yaml
```yaml
config-profiles:
- name: test-profile-v673 
  datastax-version: 6.7.3
  json:
    cassandra-yaml: 
      authenticator: com.datastax.bdp.cassandra.auth.DseAuthenticator
      num_tokens: 256
      allocate_tokens_for_local_replication_factor: 2
      endpoint_snitch: org.apache.cassandra.locator.GossipingPropertyFileSnitch
    dse-yaml: 
      authorization_options: 
        enabled: true
      authentication_options: 
        enabled: true
      dsefs_options:
        enabled: true
```

datacenters.yaml
```yaml
datacenters:
- name: test-datacenter
```

test-cluster.yaml
```yaml
clusters:
- name: test-cassandra-cluster
  comment: Test Cassandra Cluster
  repository-id: test-repository
  config-profile-id: test-profile-v673
  ssh-management-port: 22
  managed: true
  datacenter: test-datacenter
  
  nodes:
  - name: test-cluster-node-01
    ssh-management-address: 172.19.0.4
    seed: true

  - name: test-cluster-node-02
    ssh-management-address: 172.19.0.5
    seed: true

  - name: test-cluster-node-03
    ssh-management-address: 172.19.0.2
    seed: true
```
