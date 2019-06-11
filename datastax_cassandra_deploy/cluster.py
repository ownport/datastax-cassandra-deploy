
import json
import logging
import requests

from datastax_cassandra_deploy.opscenter import OpsCenterAPI

logger = logging.getLogger(__name__)


class Cluster(OpsCenterAPI):

    ENDPOINT_URI = '/api/v2/lcm/clusters/'

    def filter(self, by_name=None):
        ''' return filtered clusters list
        '''
        if by_name:
            return [cluster for cluster in self.get().get('results', []) if cluster.get('name') == by_name ]
        return []

    def get(self):
        ''' return the list of clusters
        '''
        return self._get() 

    def add(self, **kwargs):
        ''' add cluster
        '''
        clusters = self.get()
        if not clusters:
            logger.warning('Cannot get the clusters list')
            return None

        founded_clusters = [ cluster for cluster in clusters.get('results', []) if cluster.get('name', None) == kwargs.get('name') ]
        if not founded_clusters:
            created_cluster = self._add(**kwargs)
            if created_cluster:
                return created_cluster
        else:
            logger.warning('The cluster with the name {} already exists'.format(kwargs.get('name')))
        
        return None


