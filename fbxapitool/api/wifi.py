class Wifi:
    '''
    API to manage WiFi
    '''

    def __init__(self, access):
        self._access = access

    access_types = [ 'net_only', 'full' ]
    custom_key_write_parms = { 'access_type': 'text', 'description': 'text', 'duration': 'int', 'key': 'text', 'max_use_count': 'int' }
    custom_key_data_schema = { 'access_type': access_types[0], 'description': '', 'duration': 0, 'key': '', 'max_use_count': 128 }
    mac_filters = [ 'blacklist', 'whitelist' ]
    mac_filter_write_parms = { 'comment': 'text', 'type': 'text' }    
    mac_filter_data_schema = { 'comment': '', 'type': mac_filters[0] }
    mac_filter_states = [ 'disabled', 'whitelist', 'blacklist' ]
    wifi_config_write_parms = { 'enabled': 'bool', 'mac_filter_state': 'text' }
    wifi_configuration_data_schema = { 'enabled': True, 'mac_filter_state': mac_filter_states[1] }
    ap_bands = [ '2d4g', '5g', '60g' ]
    ap_channel_widths = [ 20, 40, 80, 160 ]
    ap_config_write_parms = { 'band': 'text', 'channel_width': 'int', 'primary_channel': 'int',
                             'secondary_channel': 'int', 'dfs_enabled': 'bool' }
    ap_configuration_data_schema = { 'band': ap_bands[0], 'channel_width': ap_channel_widths[0], 'primary_channel': 0,
                                    'secondary_channel': 0, 'dfs_enabled': False}
    apht_config_write_parms = { 'ac_enabled': 'bool', 'ht_enabled': 'bool',  'greenfield': 'bool', 'shortgi20': 'bool',
                               'vht_rx_ldpc': 'bool', 'ldpc': 'bool', 'vht_rx_stbc': 'text', 'vht_shortgi80': 'bool',
                               'rx_stbc': 'int', 'dsss_cck_40': 'bool', 'tx_stbc': 'bool', 'smps': 'text',
                               'vht_shortgi160': 'bool', 'vht_mu_beamformer': 'bool', 'vht_tx_stbc': 'bool',
                               'vht_su_beamformee': 'bool', 'vht_su_beamformer': 'bool', 'delayed_ba': 'bool',
                               'vht_tx_antenna_consistency': 'bool', 'max_amsdu_7935': 'bool',
                               'vht_max_ampdu_len_exp': 'int', 'vht_max_mpdu_len': 'text', 'psmp': 'bool',
                               'shortgi40': 'bool', 'vht_rx_antenna_consistency': 'bool', 'lsig_txop_prot': 'bool' }
    apht_configuration_data_schema = { 'ac_enabled': False, 'ht_enabled': True,  'greenfield': False, 'shortgi20': True,
                                      'vht_rx_ldpc': False, 'ldpc': False, 'vht_rx_stbc': 'disabled',
                                      'vht_shortgi80': False, 'rx_stbc': 1, 'dsss_cck_40': False, 'tx_stbc': True,
                                      'smps': 'disabled', 'vht_shortgi160': False, 'vht_mu_beamformer': False,
                                      'vht_tx_stbc': False, 'vht_su_beamformee': False, 'vht_su_beamformer': False,
                                      'delayed_ba': False, 'vht_tx_antenna_consistency': False, 'max_amsdu_7935': False,
                                      'vht_max_ampdu_len_exp': 0, 'vht_max_mpdu_len': 'default', 'psmp': False,
                                      'shortgi40': True, 'vht_rx_antenna_consistency': False, 'lsig_txop_prot': False }
    encryptions = [ 'wpa2_psk_ccmp', 'wpa23_psk_ccmp', 'wpa2_psk_tkip', 'wpa2_psk_auto', 'wpa12_psk_auto', 'wpa_psk_ccmp', 'wpa_psk_tkip', 'wpa_psk_auto', 'wep' ]
    bss_config_write_parms = { 'enabled': 'bool', 'wps_enabled': 'bool', 'encryption': 'text', 'hide_ssid': 'bool',
                              'eapol_version': 'int', 'key': 'text', 'ssid': 'text' }
    bss_configuration_data_schema = { 'enabled': True, 'wps_enabled': True, 'encryption': encryptions[0],
                                     'hide_ssid': False, 'eapol_version': 2, 'key': '', 'ssid': '' }
    planning_write_parms = { 'mapping': 'list' }
    planning_configuration_schema = { 'use_planning': False, 'mapping': [] }
    

    def set_ap(self, ap_id, conf):
        '''
        Updates wifi access point with the specific id
        '''
        return self._access.put('wifi/ap/{0}'.format(ap_id), { 'config': conf })

    def get_bss_list(self):
        '''
        Gets wifi BSS list
        '''
        return self._access.get('wifi/bss/')

    def get_bss(self, ap_id):
        '''
        Gets wifi BSS with the specific id
        '''
        return self._access.get('wifi/bss/{0}'.format(ap_id))

    def set_bss(self, bss_id, conf, shared = True):
        '''
        Updates wifi BSS with the specific id
        '''
        return self._access.put('wifi/bss/{0}'.format(bss_id), { 'use_shared_params': shared, 'config': conf })

    def create_wifi_custom_key(self, custom_key):
        '''
        Creates wifi custom key
        '''
        return self._access.post('wifi/custom_key/', custom_key)

    def create_wifi_mac_filter(self, mac_addr='', mac_filter=mac_filter_data_schema):
        '''
        Creates wifi mac filter
        '''
        mac_filter['mac'] = mac_addr
        return self._access.post('wifi/mac_filter/', mac_filter)

    def get_wifi_custom_key(self, key_id):
        '''
        Gets wifi custom key
        '''
        return self._access.get('wifi/custom_key/{0}'.format(key_id))

    def get_wifi_mac_filter(self, filter_id):
        '''
        Gets wifi mac filter
        '''
        return self._access.get('wifi/mac_filter/{0}'.format(filter_id))

    def delete_wifi_custom_key(self, key_id):
        '''
        Deletes wifi custom key
        '''
        return self._access.delete(f"wifi/custom_key/{key_id}")

    def delete_wifi_mac_filter(self, filter_id):
        '''
        Deletes wifi mac filter
        '''
        return self._access.delete(f"wifi/mac_filter/{filter_id}")

    def delete_wps_sessions(self):
        '''
        Deletes wps sessions
        '''
        return self._access.delete('wifi/wps/sessions')

    def set_wifi_mac_filter(self, mac_filter, wifi_mac_filter):
        '''
        Sets wifi mac filter
        '''
        return self._access.put(f"wifi/mac_filter/{mac_filter}", wifi_mac_filter)

    def get_ap(self, ap_id):
        '''
        Gets wifi access point with the specific id
        '''
        return self._access.get(f"wifi/ap/{ap_id}")

    def get_ap_allowed_channel(self, ap_id):
        '''
        Gets allowed channels of the wifi access point
        '''
        return self._access.get(f"wifi/ap/{ap_id}/allowed_channel_comb/")

    def get_wifi_access_point_channel_usage(self, ap_id):
        '''
        gets wifi access point channel usage
        '''
        return self._access.get(f"wifi/ap/{ap_id}/channel_usage/")

    def get_ap_neighbors(self, ap_id):
        '''
        Gets the list of Wifi neighbors seen by the AP
        '''
        return self._access.get(f"wifi/ap/{ap_id}/neighbors/")

    def get_wifi_access_point_station(self, ap_id, mac):
        '''
        gets wifi access point station
        '''
        return self._access.get(f"wifi/ap/{ap_id}/stations/{mac}")

    def get_station_list(self, ap_id):
        '''
        Gets the list of Wifi Stations associated to the AP
        '''
        return self._access.get(f"wifi/ap/{ap_id}/stations/")

    def get_ap_list(self):
        '''
        Gets wifi access points list
        '''
        return self._access.get('wifi/ap/')

    def get_global_config(self):
        '''
        Gets wifi global configuration
        '''
        return self._access.get('wifi/config/')

    def get_wifi_custom_keys(self):
        '''
        Gets wifi custom keys
        '''
        return self._access.get('wifi/custom_key/')

    def get_wifi_mac_filters(self):
        '''
        Gets wifi mac filters
        '''
        return self._access.get('wifi/mac_filter/')

    def get_wifi_planning(self):
        '''
        Gets wifi planning
        '''
        return self._access.get('wifi/planning/')

    def get_wps_candidates(self):
        '''
        Gets wps candidates
        '''
        return self._access.get('wifi/wps/candidates/')

    def get_wps_session(self, session_id):
        '''
        Gets wps session
        '''
        return self._access.get(f"wifi/wps/sessions/{session_id}")

    def get_wps_sessions(self):
        '''
        Gets wps sessions
        '''
        return self._access.get('wifi/wps/sessions/')

    def reset_wifi_configuration(self):
        '''
        Resets wifi configuration
        '''
        return self._access.put('wifi/config/reset/')

    def set_global_config(self, global_configuration):
        '''
        Updates wifi global configuration
        '''
        return self._access.put('wifi/config/', global_configuration)

    def set_wifi_planning(self, enabled = False, wifi_planning={}):
        '''
        Sets wifi planning
        '''
        if enabled: wifi_planning['use_planning'] = True
        else: wifi_planning = { 'use_planning': False }
        return self._access.put('wifi/planning/', wifi_planning)

    def start_wifi_access_point_neighbors_scan(self, ap_id):
        '''
        Starts wifi access point neighbors scan
        '''
        return self._access.post(f"wifi/ap/{ap_id}/neighbors/scan/")

    def get_wps_status(self):
        '''
        Gets the WPS global status
        '''
        return self._access.get('wifi/wps/config/')
    
    def set_wps_status(self, enabled = False):
        '''
        Sets the WPS global status
        '''
        return self._access.put('wifi/wps/config/', { 'enabled': enabled })
    
    def start_wps_session(self, bssid):
        '''
        Starts WPS session
        '''
        return self._access.post('wifi/wps/start/', { 'bssid': bssid })

    def stop_wps_session(self, session_id):
        '''
        Stops WPS session
        '''
        return self._access.post('wifi/wps/stop/', { 'session_id': session_id })
