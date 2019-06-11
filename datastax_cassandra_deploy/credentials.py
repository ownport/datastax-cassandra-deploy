

import os
import json
import logging
import requests

from datastax_cassandra_deploy.opscenter import OpsCenterAPI
from datastax_cassandra_deploy.utils import remove_none_values
from datastax_cassandra_deploy.utils import hide_sensetive_fields

logger = logging.getLogger(__name__)


def read_file(filepath):
    ''' return file content
    '''
    if not os.path.exists(filepath):
        logger.error('The file does not exists, {}'.format(filepath))
        return None

    filepath = os.path.abspath(filepath)
    with open(filepath, 'r') as _file:
        content = _file.read()
    
    return content


class Credentials(OpsCenterAPI):
    ''' Machine Credentials
     
    Machine Credentials contain the necessary information for logging into remote hosts as well as how to 
    escalate privileges (sudo/su).
    '''
    ENDPOINT_URI = '/api/v2/lcm/machine_credentials/'

    def get(self):
        ''' return the list of credentials
        '''
        return self._get()

    def add(self, **kwargs):
        ''' add credentials
        '''
        creds = self.get()
        if not creds:
            logger.warning('Cannot get the credentials list')
            return None

        founded_creds = [ cred for cred in creds.get('results', []) if cred.get('name', None) == kwargs.get('name') ]
        if not founded_creds:
            if kwargs.get('ssh-private-key', None):
                kwargs['ssh-private-key'] = read_file(kwargs.get('ssh-private-key'))

            created_creds = self._add(**kwargs)
            if created_creds:
                return created_creds
        else:
            logger.warning('The credentials with the name {} already exists'.format(kwargs.get('name')))
        
        return None


