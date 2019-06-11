
import json
import logging

from datastax_cassandra_deploy.opscenter import OpsCenterAPI


logger = logging.getLogger(__name__)


class InstallActions(OpsCenterAPI):

    ENDPOINT_URI = '/api/v2/lcm/actions/install'
    
    JOB_TEMPLATE = {
        "job-type":             "install",
        "job-scope":            None,
        "resource-id":          None,
        "auto-bootstrap":       False,
        "continue-on-error":    False,
        "concurrency-strategy": "default"
    }

    def install_datacenter(self, datacenter_id):
        ''' add the job for datacenter installation
        '''
        job_params = self.JOB_TEMPLATE.copy()
        job_params['job-scope'] = 'datacenter'
        job_params['resource-id'] = datacenter_id
        return self._add(**job_params)

    def install_cluster(self, cluster_id):
        ''' add the job for cluster installation
        '''
        job_params = self.JOB_TEMPLATE.copy()
        job_params['job-scope'] = 'cluster'
        job_params['resource-id'] = cluster_id
        return self._add(**job_params)


