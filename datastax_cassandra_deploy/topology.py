
import logging

from datastax_cassandra_deploy.node import Node
from datastax_cassandra_deploy.cluster import Cluster
from datastax_cassandra_deploy.opscenter import OpsCenter
from datastax_cassandra_deploy.config import ConfigProfile
from datastax_cassandra_deploy.datacenter import DataCenter
from datastax_cassandra_deploy.repository import Repository
from datastax_cassandra_deploy.credentials import Credentials

logger = logging.getLogger(__name__)


def get_resource_by_name(name, resources):
    ''' find resource by name
    '''
    for resource in resources.get().get('results', []):
        if resource.get('name') == name:
            return resource
    return {}


class Topology():

    def __init__(self, deployments):
        
        self._deployments = deployments
        self.opscenter      = None

    def deploy(self):
        ''' deploy
        '''
        if not self.connect():
            logger.error('Cannot connect to OpsCenters')
            return
        
        self.deploy_credentials()
        self.deploy_config_profiles()
        self.deploy_repositories()
        self.deploy_clusters()

    def connect(self):
        ''' connect to OpsCenter
        '''
        self.opscenter = OpsCenter(
            hostname    = self._deployments.get('opscenter', {}).get('hostname'),
            username    = self._deployments.get('opscenter', {}).get('username'),
            password    = self._deployments.get('opscenter', {}).get('password')
        )
        if self.opscenter.connect(
            timeout     = self._deployments.get('opscenter', {}).get('timeout'), 
            attempts    = self._deployments.get('opscenter', {}).get('attempts')):
        
            return True

        return False    

    def deploy_credentials(self):
        ''' deploy credentials
        '''
        credentials = Credentials(self.opscenter.url, self.opscenter.session)
        for creds in self._deployments.get('credentials', []):
            created_creds = credentials.add(**creds)
            if created_creds:
                logger.info(created_creds)

    def deploy_config_profiles(self):
        ''' deploy config profiles
        '''
        config_profiles = ConfigProfile(self.opscenter.url, self.opscenter.session)
        for conf_profile in self._deployments.get('config-profiles', []):
            created_conf_profile = config_profiles.add(**conf_profile)
            if created_conf_profile:
                logger.info(created_conf_profile)

    def deploy_repositories(self):
        ''' deploy repositories
        '''
        repositories = Repository(self.opscenter.url, self.opscenter.session)
        for repo in self._deployments.get('repositories', []):
            created_repo = repositories.add(**repo)
            if created_repo:
                logger.info(created_repo)

    def deploy_clusters(self):
        ''' deploy clusters
        '''
        clusters            = Cluster(self.opscenter.url, self.opscenter.session)
        config_profiles     = ConfigProfile(self.opscenter.url, self.opscenter.session)
        repositories        = Repository(self.opscenter.url, self.opscenter.session)
        datacenters         = DataCenter(self.opscenter.url, self.opscenter.session)
        nodes               = Node(self.opscenter.url, self.opscenter.session)

        for cluster in self._deployments.get('clusters', []):

            cluster_nodes = cluster.pop('nodes', [])
            datacenter = cluster.pop('datacenter')
            
            config = get_resource_by_name( cluster.get('config-profile-id', None), config_profiles)
            cluster['config-profile-id'] = config.get('id', 'Unknown')

            repo = get_resource_by_name( cluster.get('repository-id', None), repositories)
            cluster['repository-id'] = repo.get('id', 'Unknown')

            created_cluster = clusters.add(**cluster)
            if not created_cluster:
                created_cluster = get_resource_by_name(cluster.get('name'), clusters)
                if not created_cluster:
                    logger.error('Cannot create cluster, {}'.format(cluster))
                    continue

            created_datacenter = datacenters.add(**{ 'name': datacenter, 'cluster-id': created_cluster['id'] })
            if not created_datacenter:
                created_datacenter = get_resource_by_name(datacenter, datacenters)
                if not created_datacenter:
                    logger.error('Cannot create datacenter, name: {}, cluster: {}'.format(datacenter, created_cluster))
                    continue

            for node in cluster_nodes:
                node['datacenter-id'] = created_datacenter['id']
                created_node = nodes.add(**node)
                if not created_node:
                    created_node = get_resource_by_name(node['name'], nodes)
                    if not created_node:
                        logger.error('Cannot create node, {}'.format(node))
                        continue
                
