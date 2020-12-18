import requests
import json
from urllib.parse import urljoin
from fbxapitool.exceptions import *

class Access:
    def __init__(self, session, base_url, session_token, http_timeout):
        self.session = session
        self.header = {'X-Fbx-App-Auth': session_token}
        self.base_url = base_url
        self.timeout = http_timeout


    def get(self, end_url):
        '''
        Sends get request and return results
        '''
        url = urljoin(self.base_url, end_url)
        r = self.session.get(url, headers=self.header, timeout=self.timeout)
        resp = r.json()
        if resp['success'] != True:
            raise HttpRequestError(resp['error_code'])
        if 'result' in resp:
            return resp['result']

    def post(self, end_url, payload=None, raw=False):
        '''
        Sends post request and return results
        '''
        url = urljoin(self.base_url, end_url)
        head = self.header
        if raw:
            head['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
            data = payload
        else: data = json.dumps(payload) if payload is not None else None
        r = self.session.post(url, headers=head, data=data, timeout=self.timeout)
        resp = r.json()
        if resp['success'] != True:
            raise HttpRequestError(resp['error_code'])
        if 'result' in resp:
            return resp['result']

    def put(self, end_url, payload=None):
        '''
        Sends put request and return results
        '''
        url = urljoin(self.base_url, end_url)
        data = json.dumps(payload) if payload is not None else None
        r = self.session.put(url, headers=self.header, data=data, timeout=self.timeout)
        resp = r.json()
        if resp['success'] != True:
            raise HttpRequestError(resp['error_code'])
        if 'result' in resp:
            return resp['result']

    def delete(self, end_url, payload=None):
        '''
        Sends delete request and return results
        '''
        url = urljoin(self.base_url, end_url)
        data = json.dumps(payload) if payload is not None else None
        r = self.session.delete(url, headers=self.header, data=data, timeout=self.timeout)
        resp = r.json()
        if resp['success'] != True:
            raise HttpRequestError(resp['error_code'])
        if 'result' in resp:
            return resp['result']