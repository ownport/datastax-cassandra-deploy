
import pytest
import settings

from datastax_cassandra_deploy.opscenter import OpsCenter
from datastax_cassandra_deploy.datacenter import DataCenter
from datastax_cassandra_deploy.cluster import Cluster


def test_datacenter_init():

    opscenter = OpsCenter(settings.OPSCENTER_HOSTNAME, settings.OPSCENTER_USERNAME, settings.OPSCENTER_PASSWORD)
    assert opscenter.connect(timeout=settings.OPSCENTER_CONNECTION_TIMEOUT, attempts=settings.OPSCENTER_RETRY_ATTEMPTS)
    assert DataCenter(opscenter.url, opscenter.session)


def test_datacenter_add():

    CLUSTER_NAME = 'test-cassandra-cluster-with-datacenter'

    opscenter = OpsCenter(settings.OPSCENTER_HOSTNAME, settings.OPSCENTER_USERNAME, settings.OPSCENTER_PASSWORD)
    assert opscenter.connect(timeout=settings.OPSCENTER_CONNECTION_TIMEOUT, attempts=settings.OPSCENTER_RETRY_ATTEMPTS)
    
    clusters = Cluster(opscenter.url, opscenter.session)
    datacenters = DataCenter(opscenter.url, opscenter.session)

    created_cluster = clusters.add(**{
        'name': CLUSTER_NAME
    })
    assert created_cluster is not None
    assert created_cluster.get('datacenter') == []
    
    created_datacenter = datacenters.add(**{
        'name': 'test-cassandra-cluster-datacenter',
        'cluster-id': created_cluster.get('id')
    })
    assert created_datacenter is not None

    for cluster in clusters.filter(by_name=CLUSTER_NAME):
        for dc in cluster.get('datacenter'):
            assert dc['id'] == created_datacenter['id']
    
