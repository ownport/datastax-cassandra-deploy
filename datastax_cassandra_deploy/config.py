
import json
import logging
import requests

from datastax_cassandra_deploy.opscenter import OpsCenterAPI
from datastax_cassandra_deploy.utils import remove_none_values
from datastax_cassandra_deploy.utils import hide_sensetive_fields


logger = logging.getLogger(__name__)


class ConfigProfile(OpsCenterAPI):

    ENDPOINT_URI = '/api/v2/lcm/config_profiles/'

    def get(self):
        ''' return the list of configs
        '''
        return self._get()

    def add(self, **kwargs):
        ''' add configuration
        '''
        configs = self.get()
        if not configs:
            logger.warning('Cannot get the configs list')
            return None

        founded_configs = [ config for config in configs.get('results', []) if config.get('name', None) == kwargs.get('name') ]
        if not founded_configs:
            created_config = self._add(**kwargs)
            if created_config:
                return created_config
        else:
            logger.warning('The configuration with the name {} already exists'.format(kwargs.get('name')))
        
        return None
