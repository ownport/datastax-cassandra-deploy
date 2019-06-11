import pytest
import logging
import settings

from datastax_cassandra_deploy.opscenter import OpsCenter
from datastax_cassandra_deploy.repository import Repository

logger = logging.getLogger(__name__)


def test_repository_init():

    opscenter = OpsCenter(settings.OPSCENTER_HOSTNAME, settings.OPSCENTER_USERNAME, settings.OPSCENTER_PASSWORD)
    assert opscenter.connect(timeout=settings.OPSCENTER_CONNECTION_TIMEOUT, attempts=settings.OPSCENTER_RETRY_ATTEMPTS)
    
    assert Repository(opscenter.url, opscenter.session)


def test_repository_add():

    opscenter = OpsCenter(settings.OPSCENTER_HOSTNAME, settings.OPSCENTER_USERNAME, settings.OPSCENTER_PASSWORD)
    assert opscenter.connect(timeout=settings.OPSCENTER_CONNECTION_TIMEOUT, attempts=settings.OPSCENTER_RETRY_ATTEMPTS)
    
    repositories = Repository(opscenter.url, opscenter.session)

    kwargs = {
        "name": "test-repository",
        "username": "test",
        "password": "test",
        "comment": "Test DataStax Repository",
    }
    created_repo = repositories.add(**kwargs)
    assert created_repo is not None
    
    repos_list = repositories.get()
    assert repos_list.get('count', 0) > 0

