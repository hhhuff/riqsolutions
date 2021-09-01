import requests


class RiskIQAPI():
    def __init__(self, api_token=None, api_key=None, url_prefix='', hostname=''):
        self._token = api_token
        self._key = api_key
        self._prefix = url_prefix
        self._hostname = hostname
        self._session = requests.Session()
        self._session.headers = {
            'Content-Type': 'application/json'
        }
    
    def configure(self, api_token, api_key):
        self._token = api_token
        self._key = api_key
    
    def _request(self, method, endpoint, payload={}, params={}):
        url = 'https://{0._hostname}/{0._prefix}/{1}'.format(self, endpoint)
        creds = (self._token, self._key)
        req = self._session.request(method, url, auth=creds)
        return req
    
    def get(self, endpoint, **kwargs):
        return self._request('GET', endpoint, payload={}, params=kwargs)
