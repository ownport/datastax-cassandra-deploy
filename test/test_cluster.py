
import pytest
import settings

from datastax_cassandra_deploy.cluster import Cluster
from datastax_cassandra_deploy.opscenter import OpsCenter


def test_cluster_init():

    opscenter = OpsCenter(settings.OPSCENTER_HOSTNAME, settings.OPSCENTER_USERNAME, settings.OPSCENTER_PASSWORD)
    assert opscenter.connect(timeout=settings.OPSCENTER_CONNECTION_TIMEOUT, attempts=settings.OPSCENTER_RETRY_ATTEMPTS)
    assert Cluster(opscenter.url, opscenter.session)


def test_cluster_add():

    CLUSTER_NAME = 'test-cassandra-cluster'

    opscenter = OpsCenter(settings.OPSCENTER_HOSTNAME, settings.OPSCENTER_USERNAME, settings.OPSCENTER_PASSWORD)
    assert opscenter.connect(timeout=settings.OPSCENTER_CONNECTION_TIMEOUT, attempts=settings.OPSCENTER_RETRY_ATTEMPTS)
    
    clusters = Cluster(opscenter.url, opscenter.session)
    created_cluster = clusters.add(**{ 'name': CLUSTER_NAME, })

    assert created_cluster is not None
    assert created_cluster.get('id') is not None
    assert created_cluster.get('datacenter') == []
    
    clusters_list = clusters.filter(by_name=CLUSTER_NAME)
    assert len(clusters_list) > 0

