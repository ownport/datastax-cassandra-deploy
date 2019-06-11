## The procedure of creation Cassandra Cluster via OpsCenter

- install OpsCenter
- configure parameters
- set new admin password
- create new Cluster
  - Adding SSH Credentials.
  - Adding a Config Profile.
  - Adding a Repository.
  - Adding a Cluster, populating it with datacenters and nodes, and starting an install job.
- trigger installation process
- Monitoring install Jobs
- update keyspaces replication factor

## Cluster Install Walk-through

This is a step-by-step sequence of API calls that simulate a typical zero-to-cluster installation workflow scenario.

- Create a Repository
- Create a Machine Credentials with appropriate settings for your cluster. You may need to create multiple if you have disparate credentials across your cluster.
- Create a Config Profile with appropriate configuration settings where you wish to override the defaults. If you wish to vary your configs for each datacenter or even at the node-level, you will need to create multiple.
- Create a Cluster model, including datacenters and nodes (see Datacenter and Node). Assign repository, machine credentials, and config profiles to the appropriate cluster model objects.
- Create an Install job.
- Watch the job (see Jobs) for status.
