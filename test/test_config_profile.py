import pytest
import logging
import settings

from datastax_cassandra_deploy.opscenter import OpsCenter
from datastax_cassandra_deploy.config import ConfigProfile 

logger = logging.getLogger(__name__)


def test_config_profile_init():

    opscenter = OpsCenter(settings.OPSCENTER_HOSTNAME, settings.OPSCENTER_USERNAME, settings.OPSCENTER_PASSWORD)
    assert opscenter.connect(timeout=settings.OPSCENTER_CONNECTION_TIMEOUT, attempts=settings.OPSCENTER_RETRY_ATTEMPTS)
    
    assert ConfigProfile(opscenter.url, opscenter.session)


def test_config_profile_add():

    opscenter = OpsCenter(settings.OPSCENTER_HOSTNAME, settings.OPSCENTER_USERNAME, settings.OPSCENTER_PASSWORD)
    assert opscenter.connect(timeout=settings.OPSCENTER_CONNECTION_TIMEOUT, attempts=settings.OPSCENTER_RETRY_ATTEMPTS)
    
    config_profiles = ConfigProfile(opscenter.url, opscenter.session)

    kwargs = {
        'name': 'test-default-profile-v673',
        'datastax-version': '6.7.3',
        'comment': 'Test config profile for DSE 6.7.3 with default parameters',
        'json': {
            'cassandra-yaml': {
                "authenticator":"com.datastax.bdp.cassandra.auth.DseAuthenticator",
                "num_tokens":8,
                "allocate_tokens_for_local_replication_factor": 2,
                "endpoint_snitch":"org.apache.cassandra.locator.GossipingPropertyFileSnitch",
                "compaction_throughput_mb_per_sec": 64
            },
            "dse-yaml": {
                "authorization_options": {"enabled": True},
                "authentication_options": {"enabled": True},
                "dsefs_options": {"enabled": True}
            }
        },
    }
    created_config_profile = config_profiles.add(**kwargs)
    assert created_config_profile is not None
    
    config_profiles_list = config_profiles.get()
    assert config_profiles_list.get('count', 0) > 0

    # for profile in config_profiles_list.get('results'):
    #     print(profile.get('href'))
    #     print(opscenter.session.get(profile.get('href')).json())
    # assert False

