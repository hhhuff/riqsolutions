import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import os
import io
from lxml import etree 
import xmltodict
import json
import functools
import time
import datetime
import logging
from logging.handlers import RotatingFileHandler
import inspect
import re

# m = re.search('\/lib\/python(.*)', os.path.dirname(inspect.getfile(inspect))).group()
# module_path = '{0}{1}/site-packages/riqsolutions/riskiqapi'.format(os.getcwd(), m)
# log_formatter = logging.Formatter('%(asctime)s %(levelname)s - %(module)s:%(funcName)s(): %(message)s')
# logFile = '{0}/log/riqsolutions.log'.format(module_path)
# my_handler = RotatingFileHandler(logFile, mode='a', maxBytes=5*1024*1024, backupCount=2, encoding=None, delay=0)
# my_handler.setFormatter(log_formatter)
# my_handler.setLevel(logging.INFO)
logger = logging.getLogger('root')
# logger.setLevel(logging.INFO)
# logger.addHandler(my_handler)
logger.info('RiskIQ Solutions API Library')


class RiskIQAPI():
    def __init__(self, api_token=None, api_key=None, proxy=None, context=None, url_prefix='', hostname=''):
        self._token = api_token
        self._key = api_key
        self._proxy = proxy
        self._context = context
        self._prefix = url_prefix
        self._hostname = hostname
        self._session = get_session(proxy=proxy)
        self._session.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'RiskIQSolutions'
        }
        

    def configure(self, api_token, api_key, proxy, context):
        self._token = api_token
        self._key = api_key
        self._proxy = proxy
        self._context = context

    def _request(self, method, endpoint, payload={}, params={}, xml=None):
        type_list= ['DOMAIN', 'HOST', 'PAGE', 'IP_BLOCK', 'IP_ADDRESS', 'CONTACT', 'SSL_CERT', 'AS']
        if 'connected' in endpoint:
            full_response = {'DOMAIN':[],'HOST':[],'PAGE':[],'IP_BLOCK':[],'IP_ADDRESS':[],'CONTACT':[],'SSL_CERT':[],'AS':[]}
        else:
            full_response = []
        page_count = 0
        this_mark = "*"
        record_counter = 0
        while True:  
            if xml is not None and xml == True:
                self._session.headers = {
                    'Content-Type': 'application/json',
                    'Accept': 'text/xml',
                    'User-Agent': 'RiskIQSolutions'
                }
            if params is not None and 'page' in params.keys():
                params['page'] = page_count
            if params is not None and 'mark' in params.keys():
                params['mark'] = this_mark
            url = 'https://{0._hostname}/{0._prefix}/{1}'.format(self, endpoint)
            logger.info('url: {0}'.format(url))
            logger.info('method: {0}'.format(method))
            # logger.info('params: {0}'.format(params))
            # logger.info('payload: {0}'.format(payload))
            creds = (self._token, self._key)
            if method == "DELETE":
                req = requests.delete(url, auth=creds, params=params, json=payload)
            else:
                req = self._session.request(method, url, auth=creds, params=params, json=payload)
                logger.info(req)
                if method == "DELETE":
                    return req
                if 'Content-Type' in req.headers.keys() and req.headers.get('Content-Type') == 'text/xml':
                    parser = etree.XMLParser(recover=True)
                    tree = etree.parse(io.StringIO(req.text), parser)
                    tree.write('{0}/tmp/tmp.xml'.format(module_path), pretty_print=True, xml_declaration=True, encoding='utf-8')
                    with open('{0}/tmp/tmp.xml'.format(module_path)) as fd:
                        temp_data = xmltodict.parse(fd.read(),attr_prefix='')
                    os.remove('{0}/tmp/tmp.xml'.format(module_path))
                    this_data = json.loads(json.dumps(temp_data))
                    
                    return this_data
                else:
                    this_data = req.json()

                if 'connected' in url:
                    moreflag = False
                    for t in type_list:
                        if t in this_data.keys():
                            if this_data.get(t)['last'] == False:
                                moreflag = True
                            if len(this_data.get(t)['content']) > 0:
                                for c in this_data.get(t)['content']:
                                    full_response.get(t).append(c)
                    if moreflag == True:
                        page_count += 1
                    else:
                        return full_response
                
                elif type(this_data) is not list and 'last' in this_data.keys():
                    this_mark = this_data['mark']
                    record_counter += this_data['numberOfElements']
                    page_count += 1
                    logger.info('Retrieved {0} of {1}'.format(record_counter, this_data['totalElements']))
                    for c in this_data.get('content'):
                        full_response.append(c)
                    if this_data.get('last') == True:
                        return full_response
                else:
                    return req
    
    def get_context(self):
        return self._context

    def get(self, endpoint, payload=None, params=None, xml=None):        
        return self._request('GET', endpoint, payload=payload, params=params, xml=xml)

    def post(self, endpoint, payload=None, params=None, xml=None):
        return self._request('POST', endpoint, payload=payload, params=params, xml=xml)

    def delete(self, endpoint, payload=None, params=None, xml=None):
        return self._request('DELETE', endpoint, payload=payload, params=params, xml=xml)
    
def get_session_adapter():
    def debug_log(f):
        @functools.wraps(f)
        def decor(*args, **kwargs):
            logger.info(f'[X] had to go into retry logic')
            return f(*args, **kwargs)
        return decor
    retry_strategy = Retry(
        total=10,
        backoff_factor=.1,
        status_forcelist=[429, 500, 502, 503, 504]
    )
    retry_strategy.increment = debug_log(retry_strategy.increment)
    return HTTPAdapter(max_retries=retry_strategy)

def get_session(proxy=None):
    session = requests.Session()
    session.mount('https://', get_session_adapter())
    if proxy is not None:
        proxies = {'https': proxy}
        session.proxies.update(proxies)
    return session
