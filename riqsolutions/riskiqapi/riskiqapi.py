import requests
import os
import io
from lxml import etree 
import xmltodict
import json


class RiskIQAPI():
    def __init__(self, api_token=None, api_key=None, url_prefix='', hostname=''):
        self._token = api_token
        self._key = api_key
        self._prefix = url_prefix
        self._hostname = hostname
        self._session = requests.Session()
        self._session.headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'RiskIQSolutions'
        }

    def configure(self, api_token, api_key):
        self._token = api_token
        self._key = api_key
    
    def _request(self, method, endpoint, payload={}, params={}, **kwargs):
        type_list= ['DOMAIN', 'HOST', 'PAGE', 'IP_BLOCK', 'IP_ADDRESS', 'CONTACT', 'SSL_CERT', 'AS']
        if 'connected' in endpoint:
            full_response = {'DOMAIN':[],'HOST':[],'PAGE':[],'IP_BLOCK':[],'IP_ADDRESS':[],'CONTACT':[],'SSL_CERT':[],'AS':[]}
        else:
            full_response = []
        page_count = 0
        while True:  
            if 'xml' in kwargs.keys() and kwargs.get('xml') == True:
                self._session.headers = {
                    'Content-Type': 'application/json',
                    'Accept': 'text/xml',
                    'User-Agent': 'RiskIQSolutions'
                }
            if params is not None and 'page' in params.keys():
                params['page'] = page_count
            url = 'https://{0._hostname}/{0._prefix}/{1}'.format(self, endpoint)

            creds = (self._token, self._key)
            req = self._session.request(method, url, auth=creds, params=params, json=payload)

            if req.status_code == 200:
                if 'Content-Type' in req.headers.keys() and req.headers.get('Content-Type') == 'text/xml':
                    parser = etree.XMLParser(recover=True)
                    tree = etree.parse(io.StringIO(req.text), parser)
                    tree.write('tmp.xml', pretty_print=True, xml_declaration=True, encoding='utf-8')
                    with open('tmp.xml') as fd:
                        temp_data = xmltodict.parse(fd.read(),attr_prefix='')
                    os.remove('tmp.xml')
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
                    page_count += 1
                    for c in this_data.get('content'):
                        full_response.append(c)
                    if this_data.get('last') == True:
                        return full_response
                else:
                    return req
            else:
                raise ValueError('Request Error: {0} - {1}'.format(req.status_code, req.content))
    
    def get(self, endpoint, **kwargs):
        if 'xml' in kwargs.keys() and kwargs.get('xml') == True:
            this_xml = True
        else:
            this_xml = False
        return self._request('GET', endpoint, payload=kwargs.get('payload'), params=kwargs.get('params'), xml=this_xml)
    
    def post(self, endpoint, **kwargs):
        if 'xml' in kwargs.keys() and kwargs.get('xml') == True:
            this_xml = True
        else:
            this_xml = False
        return self._request('POST', endpoint, payload=kwargs.get('payload'), params=kwargs.get('params'), xml=this_xml)
