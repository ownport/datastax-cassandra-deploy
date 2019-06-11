
import json
import logging
import requests

from datastax_cassandra_deploy.opscenter import OpsCenterAPI
from datastax_cassandra_deploy.utils import remove_none_values
from datastax_cassandra_deploy.utils import hide_sensetive_fields


logger = logging.getLogger(__name__)


class Node(OpsCenterAPI):

    ENDPOINT_URI = '/api/v2/lcm/nodes/'

    def get(self):
        ''' return the list of nodes
        '''
        return self._get()

    def add(self, **kwargs):
        ''' add node
        '''
        nodes = self.get()
        if not nodes:
            logger.warning('Cannot get the nodes list')
            return None

        founded_nodes = [ node for node in nodes.get('results', []) if node.get('name', None) == kwargs.get('name') ]
        if not founded_nodes:
            created_node = self._add(**kwargs)
            if created_node:
                return created_node
        else:
            logger.warning('The node with the name {} already exists'.format(kwargs.get('name')))
        
        return None

