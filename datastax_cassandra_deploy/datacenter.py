
import json
import logging
import requests

from datastax_cassandra_deploy.opscenter import OpsCenterAPI

logger = logging.getLogger(__name__)


class DataCenter(OpsCenterAPI):

    ENDPOINT_URI = '/api/v2/lcm/datacenters/'

    def get(self):
        ''' returns datacenters list
        '''
        return self._get()

    def add(self, **kwargs):
        ''' add datacenter
        '''
        datacenters = self.get()
        if not datacenters:
            logger.warning('Cannot get the datacenters list')
            return None

        founded_datacenters = [ dc for dc in datacenters.get('results', []) if dc.get('name', None) == kwargs.get('name') ]
        if not founded_datacenters:
            created_datacenter = self._add(**kwargs)
            if created_datacenter:
                return created_datacenter
        else:
            logger.warning('The datacenter with the name {} already exists'.format(kwargs.get('name')))
        
        return None
