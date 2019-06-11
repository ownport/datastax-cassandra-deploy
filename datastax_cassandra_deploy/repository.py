
import json
import logging
import requests

from datastax_cassandra_deploy.opscenter import OpsCenterAPI
from datastax_cassandra_deploy.utils import remove_none_values
from datastax_cassandra_deploy.utils import hide_sensetive_fields


logger = logging.getLogger(__name__)


class Repository(OpsCenterAPI):
    '''Repository

    Repositories contain the Debian or RPM packages that LCM uses to install DSE. DataStax public repos can be used, 
    or you can setup your own package repositories.
    '''
    ENDPOINT_URI = '/api/v2/lcm/repositories/'

    def get(self):
        ''' return the list of repositories
        '''
        return self._get()

    def add(self, **kwargs):
        ''' add repository
        '''
        repos = self.get()
        if not repos:
            logger.warning('Cannot get the repository list')
            return None

        founded_repos = [ repo for repo in repos.get('results', []) if repo.get('name', None) == kwargs['name'] ]
        if not founded_repos:
            created_repo = self._add(**kwargs)
            if created_repo:
                return created_repo
        else:
            logger.warning('The repository with the name {} already exists'.format(kwargs['name']))
        
        return None

