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
from time import perf_counter

log_formatter = logging.Formatter('%(asctime)s %(levelname)s - %(module)s:%(funcName)s(): %(message)s')
my_handler = RotatingFileHandler(
    os.path.realpath(__file__).replace('riskiqapi.py','log/riqsolutions.log'), 
    mode='a', 
    maxBytes=5*1024*1024, 
    backupCount=2, 
    encoding=None, 
    delay=0
)
my_handler.setFormatter(log_formatter)
my_handler.setLevel(logging.INFO)
logger = logging.getLogger('root')
logger.setLevel(logging.INFO)
logger.addHandler(my_handler)
logger.info('RiskIQ Solutions API Library')


class RiskIQAPI():
    def __init__(self, api_token=None, api_key=None, proxy=None, context=None, url_prefix='', hostname='', timeout=(5.0,30.0), retries=2, backoff=0.1, threadindex=None):
        self._token = api_token
        self._key = api_key
        self._proxy = proxy
        self._context = context
        self._prefix = url_prefix
        self._hostname = hostname
        self._timeout = timeout
        self._markcount = 0
        retry_strategy = Retry(
            total = retries,
            connect = 3,
            backoff_factor = backoff,
            status_forcelist = [429, 500, 502, 503, 504],
            method_whitelist = ["GET", "POST"]
        )
        self._adapter = HTTPAdapter(max_retries = retry_strategy)
        self._session = requests.Session()
        
        self._session.mount("https://", self._adapter)
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

    def _request(self, method, endpoint, payload={}, params={}, xml=None, thread_data=None):
        try:
            if xml is not None and xml == True:
                self._session.headers = {
                    'Content-Type': 'application/json',
                    'Accept': 'text/xml',
                    'User-Agent': 'RiskIQSolutions'
                }
            url = 'https://{0._hostname}/{0._prefix}/{1}'.format(self, endpoint)
            creds = (self._token, self._key)

            t1_start = perf_counter()
            if method == "DELETE":
                req = requests.delete(url, auth=creds, params=params, json=payload)
                return req
            else:
                req = self._session.request(method, url, auth=creds, params=params, json=payload, timeout=self._timeout)
            t1_stop = perf_counter()

            if thread_data != None:
                logger.info('{0}-thr:{1} -queue#:{2} -url: {3} -method: {4} - statuscode: {45} -elapsed(sec):{6}'.format(self._context,thread_data.get('threadindex'), thread_data.get('qsize'), url, method, req.status_code, t1_stop-t1_start))
            else:
                logger.info('{0}-url: {1} -method: {2} - statuscode: {3} -elapsed(sec):{4}'.format(self._context, url, method, req.status_code, t1_stop-t1_start))

            if 'Content-Type' in req.headers.keys() and req.headers.get('Content-Type') == 'text/xml':
                parser = etree.XMLParser(recover=True)
                tree = etree.parse(io.StringIO(req.text), parser)
                tree.write('{0}/tmp/tmp.xml'.format(module_path), pretty_print=True, xml_declaration=True, encoding='utf-8')
                with open('{0}/tmp/tmp.xml'.format(module_path)) as fd:
                    temp_data = xmltodict.parse(fd.read(),attr_prefix='')
                os.remove('{0}/tmp/tmp.xml'.format(module_path))
                this_data = json.loads(json.dumps(temp_data))
                return this_data
            
            if type(req.json()) is not list and 'last' in req.json().keys():
                self._markcount += req.json().get('numberOfElements')
                logger.info('{0} Retrieved {1} of {2}'.format(self._context, self._markcount, req.json().get('totalElements')))
                if req.json().get('last') == True:
                    self._markcount = 0
                
            return req
        except Exception as e:
            t1_stop = perf_counter()
            this_e = {'error':str(e),'method':method,'payload':payload,'params':params,'elapsed':t1_stop-t1_start}
            if thread_data != None:
                logger.info('{0}-thr:{1} -elapsed(sec):{2} \n - method {3} \n - payload: {4} \n - params: {5} \n - error: {6}'.format(self._context, thread_data.get('threadindex'), t1_stop-t1_start, this_e.get('error'), method, payload, params))
            else:
                logger.info('{0}-{1}'.format(self._context,this_e))
            return this_e
            
    def get_context(self):
        return self._context

    def get(self, endpoint, payload=None, params=None, xml=None, thread_data=None):
        return self._request('GET', endpoint, payload=payload, params=params, xml=xml, thread_data=thread_data)

    def post(self, endpoint, payload=None, params=None, xml=None, thread_data=None):
        return self._request('POST', endpoint, payload=payload, params=params, xml=xml, thread_data=thread_data)

    def delete(self, endpoint, payload=None, params=None, xml=None):
        return self._request('DELETE', endpoint, payload=payload, params=params, xml=xml)
    