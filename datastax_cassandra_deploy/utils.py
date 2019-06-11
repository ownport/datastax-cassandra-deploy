
import json
import yaml
import logging

logger = logging.getLogger(__name__)


def load_deployment(deployments):
    ''' reused from https://github.com/ansible/ansible/blob/devel/lib/ansible/utils/vars.py
        and modified according to DataStax Cassandra deployment requirements 
    ''' 
    result = {}

    if not deployments:
        return result

    for deployment_file in deployments:
        data = None
        # Argument is a YAML file (JSON is a subset of YAML)
        try:
            with open(deployment_file, 'r', encoding='utf8') as source:
                try:
                    deployment = yaml.load(source, Loader=yaml.FullLoader)
                except yaml.YAMLError as err:
                    logger.error('{}, {}'.format(err, _vars))
        except FileNotFoundError as err:
            logger.error(err)
            continue
        
        if deployment and isinstance(deployment, dict):
            result.update(deployment)

    return result


def pretty_json(data):
    ''' returns pretty json
    '''
    return json.dumps(data, sort_keys=True, indent=4)


def remove_none_values(params):
    ''' remove elements with None values
    '''
    if not isinstance(params, dict):
        return params

    result = dict()
    for k, v in params.items():
        if v is not None:
            result[k] = v
    return result


def hide_sensetive_fields(params):
    ''' replace sensitive information by '*'
    '''
    if not isinstance(params, dict):
        return params
    
    for k, v in params.items():
        if k in ('login-password', 'become-password', 'password'):
            params[k] = '*' * 10
    return params
