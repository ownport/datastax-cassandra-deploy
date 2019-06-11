
import pytest
import socket
import settings

from datastax_cassandra_deploy.node import Node
from datastax_cassandra_deploy.cluster import Cluster
from datastax_cassandra_deploy.datacenter import DataCenter
from datastax_cassandra_deploy.actions import InstallActions

from datastax_cassandra_deploy.opscenter import OpsCenter


def test_install_cluster():

    NODE_NAME = 'datanode-01b'

    opscenter = OpsCenter(settings.OPSCENTER_HOSTNAME, settings.OPSCENTER_USERNAME, settings.OPSCENTER_PASSWORD)
    assert opscenter.connect(timeout=settings.OPSCENTER_CONNECTION_TIMEOUT, attempts=settings.OPSCENTER_RETRY_ATTEMPTS)
    
    clusters = Cluster(opscenter.url, opscenter.session)
    created_cluster = clusters.add(**{
        'name': 'cluster-b'
    })

    datacenters = DataCenter(opscenter.url, opscenter.session)
    created_datacenter = datacenters.add(**{
        'name': 'datacenter-cluster-b', 
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
    
    actions = InstallActions(opscenter.url, opscenter.session)
    cluster_install_action = actions.install_cluster(cluster_id=created_cluster['id'])
    assert cluster_install_action is not None


def test_install_datacenter():

    NODE_NAME = 'datanode-01c'

    opscenter = OpsCenter(settings.OPSCENTER_HOSTNAME, settings.OPSCENTER_USERNAME, settings.OPSCENTER_PASSWORD)
    assert opscenter.connect(timeout=settings.OPSCENTER_CONNECTION_TIMEOUT, attempts=settings.OPSCENTER_RETRY_ATTEMPTS)
    
    clusters = Cluster(opscenter.url, opscenter.session)
    created_cluster = clusters.add(**{
        'name': 'cluster-c'
    })

    datacenters = DataCenter(opscenter.url, opscenter.session)
    created_datacenter = datacenters.add(**{
        'name': 'datacenter-cluster-c', 
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
    
    actions = InstallActions(opscenter.url, opscenter.session)
    datacenter_install_action = actions.install_datacenter(datacenter_id=created_datacenter['id'])
    assert datacenter_install_action is not None


