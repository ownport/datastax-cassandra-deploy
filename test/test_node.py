
import pytest
import socket
import settings

from datastax_cassandra_deploy.node import Node
from datastax_cassandra_deploy.datacenter import DataCenter
from datastax_cassandra_deploy.cluster import Cluster

from datastax_cassandra_deploy.opscenter import OpsCenter


def test_node_init():

    opscenter = OpsCenter(settings.OPSCENTER_HOSTNAME, settings.OPSCENTER_USERNAME, settings.OPSCENTER_PASSWORD)
    assert opscenter.connect(timeout=settings.OPSCENTER_CONNECTION_TIMEOUT, attempts=settings.OPSCENTER_RETRY_ATTEMPTS)
    assert Node(opscenter.url, opscenter.session)


def test_node_add():

    NODE_NAME = 'datanode-01a'

    opscenter = OpsCenter(settings.OPSCENTER_HOSTNAME, settings.OPSCENTER_USERNAME, settings.OPSCENTER_PASSWORD)
    assert opscenter.connect(timeout=settings.OPSCENTER_CONNECTION_TIMEOUT, attempts=settings.OPSCENTER_RETRY_ATTEMPTS)
    
    clusters = Cluster(opscenter.url, opscenter.session)
    created_cluster = clusters.add(**{
        'name': 'cluster-a'
    })

    datacenters = DataCenter(opscenter.url, opscenter.session)
    created_datacenter = datacenters.add(**{
        'name': 'datacenter-cluster-a', 
        'cluster-id': created_cluster['id'],
    })

    nodes = Node(opscenter.url, opscenter.session)
    created_node = nodes.add(**{ 
        'name': NODE_NAME, 
        'datacenter-id': created_datacenter['id'],
        'ssh-management-address': socket.gethostbyname(NODE_NAME),
        'seed': True,
        'rack': 'rack-01',
    })

    assert created_node is not None
    assert created_node.get('id') is not None
    
