import requests
import hmac
import time
import json
import ipaddress
import logging
import os
import socket
from urllib.parse import urljoin
import fbxapitool
from fbxapitool.exceptions import *
from fbxapitool.access import Access
from fbxapitool.api.system import System
from fbxapitool.api.connection import Connection
from fbxapitool.api.dhcp import Dhcp
from fbxapitool.api.switch import Switch
from fbxapitool.api.lan import Lan
from fbxapitool.api.wifi import Wifi
from fbxapitool.api.fs import Fs
from fbxapitool.api.call import Call
from fbxapitool.api.fw import Fw
from fbxapitool.api.phone import Phone
from fbxapitool.api.airmedia import Airmedia
from fbxapitool.api.freeplugs import Freeplugs
from fbxapitool.api.vm import Vm
from fbxapitool.api.contact import Contact
from fbxapitool.api.ftp import Ftp
from fbxapitool.api.home import Home
from fbxapitool.api.lcd import Lcd
from fbxapitool.api.netshare import Netshare
from fbxapitool.api.notifications import Notifications
from fbxapitool.api.parental import Parental, Profile
from fbxapitool.api.rrd import Rrd
from fbxapitool.api.storage import Storage
from fbxapitool.api.tv import Tv
from fbxapitool.api.upnpav import Upnpav
from fbxapitool.api.upnpigd import Upnpigd
from fbxapitool.api.vpn import Vpn
from fbxapitool.api.downloads import Downloads

# Default location for the Token file 
token_filename = 'app_auth'
token_dir = os.path.dirname(os.path.abspath(__file__))
token_file = os.path.join(token_dir, token_filename)

# Default application descriptor
app_desc = {
    'app_id':'fbxa',
    'app_name':'fbxapitool',
    'app_version':fbxapitool.__version__,
    'device_name':socket.gethostname()
    }

logger = logging.getLogger(__name__)

class Freebox:
    def __init__(self, app_desc=app_desc, token_file=token_file, api_version='v8', timeout=10):
        self.token_file = token_file
        self.api_version = api_version
        self.timeout = timeout
        self.app_desc = app_desc

    def open(self, host, port):
        '''
        Opens a session to the freebox, get a valid access module
        and instantiates freebox modules
        '''
        if not self._is_app_desc_valid(self.app_desc): raise InvalidTokenError('invalid application descriptor')
        self.session = requests.Session()
        self.session.verify = os.path.join(os.path.dirname(__file__), 'freebox_root_ca.pem')
        self._access = self._get_freebox_access(host, port, self.api_version, self.token_file, self.app_desc, self.timeout)
        # Instantiate Freebox API modules
        self.system = System(self._access)
        self.connection = Connection(self._access)
        self.dhcp = Dhcp(self._access)
        self.switch = Switch(self._access)
        self.lan = Lan(self._access)
        self.wifi = Wifi(self._access)
        self.fs = Fs(self._access)
        self.call = Call(self._access)
        self.fw = Fw(self._access)
        self.phone = Phone(self._access)
        self.airmedia = Airmedia(self._access)
        self.freeplugs = Freeplugs(self._access)
        self.vm = Vm(self._access)
        self.contact = Contact(self._access)
        self.ftp = Ftp(self._access)
        self.home = Home(self._access)
        self.lcd = Lcd(self._access)
        self.netshare = Netshare(self._access)
        self.notifications = Notifications(self._access)
        self.parental = Parental(self._access)
        self.profile = Profile(self._access)
        self.rrd = Rrd(self._access)
        self.storage = Storage(self._access)
        self.tv = Tv(self._access)
        self.upnpav = Upnpav(self._access)
        self.upnpigd = Upnpigd(self._access)
        self.vpn = Vpn(self._access)
        self.downloads = Downloads(self._access)

    def close(self):
        '''
        Closes the freebox session
        '''
        if self._access is None: raise NotOpenError('Freebox is Not opened')
        self._access.post('login/logout')

    def test(self, method, url, conf = None):
        '''
        Just for testing API functions with raw usage
        '''
        if method == 'get': return self._access.get(url)
        elif method == 'del': return self._access.delete(url)
        elif method == 'put': return self._access.put(url, conf)
        elif method == 'post': return self._access.post(url, conf)
        else: return self._access.post(url, conf, True)

    def _get_freebox_access(self, host, port, api_version, token_file, app_desc, timeout=10):
        '''
        Returns an access object used for HTTP requests.
        '''
        base_url = self._get_base_url(host, port, api_version)
        # Read stored application token
        logger.info('Read application authorization file')
        app_token, track_id, file_app_desc = self._readfile_app_token(token_file)
        # If no valid token is stored then request a token to freebox api - Only for LAN connection
        if app_token is None or file_app_desc != app_desc:
                logger.info('No valid authorization file found')
                # Get application token from the freebox
                app_token, track_id = self._get_app_token(base_url, app_desc, timeout)
                # Check the authorization status
                out_msg_flag = False
                status = None
                while(status != 'granted'):
                    status = self._get_authorization_status(base_url, track_id, timeout)
                    # denied status = authorization failed
                    if status == 'denied':
                        raise AuthorizationError('the app_token is invalid or has been revoked')
                    # Pending status : user must accept the app request on the freebox
                    elif status == 'pending':
                        if not out_msg_flag:
                            out_msg_flag = True
                            print('Please confirm the authentification on the freebox')
                        time.sleep(1)
                    # timeout = authorization failed
                    elif status == 'timeout':
                        raise AuthorizationError('timeout')
                logger.info('Application authorization granted')
                # Store application token in file
                self._writefile_app_token(app_token, track_id, app_desc, token_file)
                logger.info('Application token file was generated : {0}'.format(token_file))
        # Get token for the current session
        session_token, session_permissions = self._get_session_token(base_url, app_token, app_desc['app_id'], timeout)
        logger.info('Session opened')
        logger.info('Permissions: ' + str(session_permissions))
        # Create freebox http access module
        fbx_access = Access(self.session, base_url, session_token, timeout)
        return fbx_access

    def _get_authorization_status(self, base_url, track_id, timeout):
        '''
        Gets authorization status of the application token
        Returns:
            unknown 	the app_token is invalid or has been revoked
            pending 	the user has not confirmed the authorization request yet
            timeout 	the user did not confirmed the authorization within the given time
            granted 	the app_token is valid and can be used to open a session
            denied 	    the user denied the authorization request
        '''
        url = urljoin(base_url, 'login/authorize/{0}'.format(track_id))
        r = self.session.get(url, timeout=timeout)
        resp = r.json()
        return resp['result']['status']

    def _get_app_token(self, base_url, app_desc, timeout=10):
        '''
        Gets the application token from the freebox
        Returns (app_token, track_id)
        '''
        # Get authentification token
        url = urljoin(base_url, 'login/authorize/')
        data = json.dumps(app_desc)
        r = self.session.post(url, data, timeout=timeout)
        resp = r.json()
        # raise exception if resp.success != True
        if not resp.get('success'):
            raise AuthorizationError('authentification failed')
        app_token = resp['result']['app_token']
        track_id = resp['result']['track_id']
        return(app_token, track_id)

    def _writefile_app_token(self, app_token, track_id, app_desc, file):
        '''
        Stores the application token into g_app_auth_file file
        '''
        d = {**app_desc, 'app_token': app_token, 'track_id': track_id}
        with open(file, 'w') as f:
            json.dump(d, f)

    def _readfile_app_token(self, file):
        '''
        Reads the application token in g_app_auth_file file.
        Returns (app_token, track_id, app_desc)
        '''
        try:
            with open(file, 'r') as f:
                d = json.load(f)
                app_token = d['app_token']
                track_id = d['track_id']
                app_desc = {k: d[k] for k in ('app_id', 'app_name', 'app_version', 'device_name') if k in d}
                return (app_token, track_id, app_desc)
        except FileNotFoundError:
            return (None, None, None)

    def _get_session_token(self, base_url, app_token, app_id, timeout=10):
        '''
        Gets session token from freebox.
        Returns (session_token, session_permissions)
        '''
        # Get challenge from API
        challenge = self._get_challenge(base_url, timeout)
        # Hash app_token with chalenge key to get the password
        h = hmac.new(app_token.encode(), challenge.encode(), 'sha1')
        password = h.hexdigest()
        url = urljoin(base_url, 'login/session/')
        data = json.dumps({'app_id': app_id, 'password': password})
        r = self.session.post(url, data, timeout=timeout)
        resp = r.json()
        # raise exception if resp.success != True
        if not resp.get('success'):
            raise AuthorizationError('get_session_token failed')
        session_token = resp.get('result').get('session_token')
        session_permissions = resp.get('result').get('permissions')
        return(session_token, session_permissions)

    def _get_challenge(self, base_url, timeout=10):
        '''
        Returns challenge from freebox API
        '''
        url = urljoin(base_url, 'login')
        r = self.session.get(url, timeout=timeout)
        resp = r.json()
        # raise exception if resp.success != True
        if not resp.get('success'):
            raise AuthorizationError('get_challenge failed')
        return resp['result']['challenge']

    def _get_base_url(self, host, port, freebox_api_version):
        '''
        Returns base url for HTTPS requests
        '''
        return 'https://{0}:{1}/api/{2}/'.format(host, port, freebox_api_version)

    def _is_app_desc_valid(self, app_desc):
        '''
        Checks validity of the application descriptor
        '''
        if all(k in app_desc for k in ('app_id', 'app_name', 'app_version', 'device_name')):
            return True
        else:
            return False

    def encodeJSON(self, base, parms):
        '''
        Formats parms into a JSON used for API calls
        '''
        data = {}
        if len(parms) == 0: return None
        if len(parms) > len(base): return None
        for cmd in parms:
            conf_eq = cmd.find('=')
            if conf_eq <= 0: return None
            conf_parm = [ cmd[:conf_eq], cmd[conf_eq + 1:] ]
            if conf_parm[0] in base:
                typ = base[conf_parm[0]]
                if typ != 'list' and typ != 'list-multi' and typ != 'text' and conf_parm[1] == '': return None
                if typ == 'bool': data[conf_parm[0]] = (conf_parm[1] == 'True')
                elif typ == 'int': data[conf_parm[0]] = int(conf_parm[1])
                elif typ == 'list':
                    data[conf_parm[0]] = conf_parm[1].split(',')
                    if data[conf_parm[0]] == ['']: data[conf_parm[0]]=[]
                elif typ == 'list-multi':
                    val = []
                    for item in conf_parm[1].split(','):
                        slist = {}
                        for sub in item.split(';'):
                            final = sub.split('#')
                            slist[final[0]] = final[1]
                        val.append(slist)
                    data[conf_parm[0]] = val
                elif typ == 'sublist':
                    slist = {}
                    for sub in conf_parm[1].split(';'):
                        final = sub.split('#')
                        slist[final[0]] = final[1]
                    data[conf_parm[0]] = slist
                else: data[conf_parm[0]] = conf_parm[1]
            else: return None
        return data
