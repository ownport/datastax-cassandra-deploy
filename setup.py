
import os
import sys
from codecs import open

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md'), 'r', 'utf-8') as handle:
    readme = handle.read()

setup(
    name = 'datastax-cassandra-deploy',
    version = '0.1.0.dev0',
    description = "DataStax Cassandra Deployment scripts",
    long_description = readme,
    packages=find_packages('datastax_cassandra_deploy'),
    python_requires = '>=3.5',
    install_requires = [
        'requests==2.22.0',
        'PyYAML==5.1.1',
    ],
    entry_points = {
        'console_scripts': [ 'ds-cas-deploy=datastax_cassandra_deploy.cli:launch_new_instance' ]
    }
)
