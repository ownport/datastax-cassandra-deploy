
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
        parser.add_argument('-a', '--action', default='deploy',
                            help='Actions: deploy | dump')
        parser.add_argument('-s', '--section', action='append',
                            help='The section for config dump. Possible values: credentials, config-profiles, datacenters, repositories, clusters')
        parser.add_argument('-o', '--output', 
                            help='The output path for config dump')
        parser.add_argument('-d', '--deployment', dest="deployment", action="append",
                            help="the path to deployment configuration. Support YAML/JSON file",
                            default=[])
        
        args = parser.parse_args()

        logging.basicConfig(level=args.log_level,
                            format="%(asctime)s.%(msecs)03d (%(name)s) [%(levelname)s] %(message)s",
                            datefmt='%Y-%m-%dT%H:%M:%S')

        self.action         = args.action
        self.sections       = args.section
        self.output         = args.output
        self.deployments    = load_deployment(args.deployment)


    def run(self):
        ''' run action
        '''
        if self.action == 'dump':
            logger.info('Dumping deployment configs from DataStax OpsCenter')
            self.dump(self.sections, self.output)

        elif self.action == 'deploy':
            self.deploy()

        else:
            logger.error('Unknown action: {}'.format(self.action))

    def deploy(self):
        ''' deploy topology 
        '''
        logger.info('Deployment started')
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
        logger.info('Deployment completed')

    def dump(self, sections, output):
        ''' dump topology 
        '''
        logger.info('Dumping started')
        try:
            topology = Topology(self.deployments)
            topology.dump(sections, output)

        except IOError as err:
            logger.info(err)
            sys.exit(1)

        except TypeError as err:
            logger.error(err)
            sys.exit(2)

        except KeyboardInterrupt as err:
            logger.info('The processing was interrupted by user')
            sys.exit(3)
        logger.info('Dumping completed')



def launch_new_instance():
    ''' launch new CLI instance
    '''
    cli = CLI() 
    cli.run()


if __name__ == '__main__':

    launch_new_instance()
