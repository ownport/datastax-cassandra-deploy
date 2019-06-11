
import json
import logging
import requests

from datastax_cassandra_deploy.opscenter import OpsCenterAPI
from datastax_cassandra_deploy.utils import remove_none_values
from datastax_cassandra_deploy.utils import hide_sensetive_fields


logger = logging.getLogger(__name__)


def runningJob(jobs):
    running = False
    for r in jobs['results']:
        if r['status'] == 'RUNNING' or r['status'] == 'PENDING' or r['status'] == 'WILL_FAIL':
            return True


class Job(OpsCenterAPI):

    ENDPOINT_URI = '/api/v2/lcm/jobs/'

    def get(self):
        ''' returns the jobs list
        '''
        return self._get()
