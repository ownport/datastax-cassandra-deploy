
import os
import sys
import logging
import argparse

from datastax_cassandra_deploy.utils import load_deployment
from datastax_cassandra_deploy.topology import Topology

logger = logging.getLogger(__name__)


class CLI(object):

    def __init__(self):

        parser = argparse.ArgumentParser()

        parser.add_argument('-v', '--version', action='version',
                            version='ds-cas-deploy, v{}'.format('0.1.0.dev0'))
        parser.add_argument('-l', '--log-level', default='INFO',
                            help='Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL')
        parser.add_argument('-d', '--deployment', dest="deployment", action="append",
                            help="the path to deployment configuration. Support YAML/JSON file",
                            default=[])
        
        args = parser.parse_args()

        logging.basicConfig(level=args.log_level,
                            format="%(asctime)s.%(msecs)03d (%(name)s) [%(levelname)s] %(message)s",
                            datefmt='%Y-%m-%dT%H:%M:%S')

        self.deployments = load_deployment(args.deployment)

    def deploy(self):
        ''' deploy topology 
        '''
        try:
            topology = Topology(self.deployments)
            topology.deploy()

        except IOError as err:
            logger.info(err)
            sys.exit(1)

        except TypeError as err:
            logger.error(err)
            sys.exit(2)

        except KeyboardInterrupt as err:
            logger.info('The processing was interrupted by user')
            sys.exit(3)

    
def launch_new_instance():

    cli = CLI() 
    logger.info('Deployment started')
    cli.deploy()
    logger.info('Deployment completed')


if __name__ == '__main__':

    launch_new_instance()
