
import pytest
import logging
import settings

from datastax_cassandra_deploy.opscenter import OpsCenter
from datastax_cassandra_deploy.credentials import Credentials

logger = logging.getLogger(__name__)


def test_credentials_init():

    opscenter = OpsCenter(settings.OPSCENTER_HOSTNAME, settings.OPSCENTER_USERNAME, settings.OPSCENTER_PASSWORD)
    assert opscenter.connect(timeout=settings.OPSCENTER_CONNECTION_TIMEOUT, attempts=settings.OPSCENTER_RETRY_ATTEMPTS)
    
    assert Credentials(opscenter.url, opscenter.session)


def test_credentials_add():

    opscenter = OpsCenter(settings.OPSCENTER_HOSTNAME, settings.OPSCENTER_USERNAME, settings.OPSCENTER_PASSWORD)
    assert opscenter.connect(timeout=settings.OPSCENTER_CONNECTION_TIMEOUT, attempts=settings.OPSCENTER_RETRY_ATTEMPTS)
    
    creds = Credentials(opscenter.url, opscenter.session)

    kwargs = {
        "name": "test-ssh-creds",
        "become-mode": "sudo",
        "use-ssh-keys": True,
        "login-user": "cassandra",
        "ssh-private-key": "test/resources/keys/cassandra",
    }
    created_creds = creds.add(**kwargs)
    assert created_creds is not None
    
    creds_list = creds.get()
    assert creds_list.get('count', 0) > 0

