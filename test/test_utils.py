

from datastax_cassandra_deploy.utils import pretty_json


def test_pretty_json():

    assert pretty_json({}) == '{}'
