
import json
import time
import logging
import requests

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from requests.packages.urllib3.exceptions import InsecureRequestWarning


logger = logging.getLogger(__name__)


class OpsCenter(object):
    """ Class to contain OpsCenter session state 
    """
    def __init__(self, hostname, username, password):

        self._hostname   = hostname
        self._url        = "http://" + hostname + ":8888"
        self._username   = username
        self._password   = password

        self._session    = requests.Session()
        
        # Explicitly ignoring self-signed SSL certs, this prints warnings
        self._session.verify = False
        
        # supress warnings
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        
        # These scripts don't create new sessions, therefore we're setting the
        # retry logic here. The adapter mounting means any http(s) calls will
        # retry with an exponential backoff
        retries = 10,
        backoff_factor = 0.1,
        status_forcelist = (500, 502, 504)
        
        retry = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
        )
        adapter = HTTPAdapter(max_retries=retry)
        self._session.mount('http://', adapter)
        self._session.mount('https://', adapter)

    @property
    def session(self):
        return self._session

    @property
    def url(self):
        return self._url

    def connect(self, timeout, attempts):
        ''' connect to OpsCenter
        '''
        count = 0
        while True:
            count += 1
            if count > attempts:
                logger.error("OpsCenter connection failed after {n} attempts".format(n=attempts))
                break
                
            try:
                logger.info("Trying to {url}/meta".format(url=self._url))
                meta = self._session.get("{url}/meta".format(url=self._url), timeout=timeout)

            except requests.exceptions.Timeout as e:
                logger.warning("OpsCenter connection timeout, attempt: {attempt}, wait {timeout} sec...".format(
                    attempt=count, timeout=timeout))
                if count < attempts:
                    time.sleep(timeout)
                continue

            except requests.exceptions.ConnectionError as e:
                logger.warning("OpsCenter connection refused, attempt: {attempt}, wait {timeout} sec...".format(
                    attempt=count, timeout=timeout))
                if count < attempts:
                    time.sleep(timeout)
                continue

            except Exception as e:
                logger.warning("OpsCenter connection failed, attempt: {attempt}, wait {timeout} secs...".format(
                    attempt=count, timeout=timeout))
                if count < attempts:
                    time.sleep(timeout)
                continue

            if (len(meta.history) > 0) and meta.history[0].status_code == 302:
                self._url = "https://" + self._hostname + ":8443"
                logger.info("Redirecting to {url}".format(url=self._url))

            if meta.status_code == 200:
                data = meta.json()
                logger.info("The connection to OpsCenter was established, the OpsCenter version: {version}".format(version=data['version']))
                return True

            if meta.status_code == 401:
                logger.info("OpsCenter Auth enabled, attempting login...")
                resp = self.login(timeout, attempts)
                if resp == None:
                    logger.error("OpsCenter Authetication was failed")
                    break

        return False

    def login(self, timeout, attempts):
        count = 0
        while count < attempts:
            resp = self._session.post(
                            "{url}/login".format(url=self._url), 
                            data={"username":self._username, "password":self._password}, 
                            timeout=timeout)
            if resp.status_code == 200:
                self._session.headers.update(resp.json())
                return resp
            else:
                logger.warning("OpsCenter login failed, attempt: {count} response: {response}, retry after 10 secs".format(
                    count=count, response=resp.json()))
                time.sleep(10)
            count += 1
        logger.error("OpsCenter connection failed after {n} attempts".format(n=attempts))
        return None


class OpsCenterAPI(object):

    ENDPOINT_URI = 'UNSPECIFIED'

    def __init__(self, opscenter_url, session):

        if not opscenter_url:
            raise ValueError('The OpsCenter URL is not specified, url: {urs}'.format(url=opscenter_url))
        self.url = opscenter_url

        if not session:
            raise RuntimeError('No connection to OpsCenter, session: {session}'.format(session=session))
        self.session = session

    def _get(self):
        ''' return resources by HTTP GET
        '''
        try:
            return self.session.get("{url}{endpoint}".format(url=self.url, endpoint=self.ENDPOINT_URI)).json()

        except requests.exceptions.Timeout as e:
            logger.error("Connection timeout, error: {}".format(e))
            return False

        except requests.exceptions.ConnectionError as e:
            logger.error("Connection error, error: {}".format(e))
            return False

        except Exception as e:
            raise RuntimeError('Unhandled error, err: {}'.format(e))

    def _add(self, **kwargs):
        ''' add resource by HTTP POST
        '''
        try:
            response = self.session.post("{url}{endpoint}".format(url=self.url, endpoint=self.ENDPOINT_URI), data=json.dumps(kwargs))
            if response.status_code != 201:
                logger.error('Cannot create the resource, {}'.format(json.dumps({
                    'endpoint uri': self.ENDPOINT_URI,
                    'method': 'POST',
                    'status code': response.status_code,
                    'response': response.text,
                    'parameters': kwargs,
                })))
                return None 
            return response.json()

        except requests.exceptions.Timeout as e:
            logger.error("Connection timeout, error: {}".format(e))
            return None

        except requests.exceptions.ConnectionError as e:
            logger.error("Connection error, error: {}".format(e))
            return None

        except Exception as e:
            raise RuntimeError('Unhandled error, err: {}'.format(e))

