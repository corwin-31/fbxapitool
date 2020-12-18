class Phone:
    '''
    API to manage phones
    Warning : partially tested
    '''

    def __init__(self, access):
        self._access = access

    dect_write_parms = { 'dect_enabled': 'bool', 'dect_registration': 'bool', 'dect_eco_mode': 'bool', 'dect_pin': 'int', 'dect_ring_pattern': 'int', 'dect_nemo_mode': 'bool', 'dect_registration': 'bool', 'dect_ring_on_off': 'bool' }
    dect_configuration_schema = { 'dect_enabled': False, 'dect_registration': False, 'dect_eco_mode': True, 'dect_pin': 2152, 'dect_ring_pattern': 1, 'dect_nemo_mode': True, 'dect_registration': False, 'dect_ring_on_off': True }


    def get_list(self):
        '''
        Gets phone list:
        '''
        return self._access.get('phone/')

    def get_config(self):
        '''
        Gets phone configuration
        '''
        return self._access.get('phone/config/')

    def set_config(self, conf):
        '''
        Updates phone configuration:
        '''
        return self._access.put('phone/', conf)

    def get_dect_vendors(self):
        '''
        Gets phone configuration:
        '''
        return self._access.get('phone/dect_vendors/')

    def start_dect_configuration(self, dect_configuration=dect_configuration_schema):
        '''
        Starts dect configuration
        '''
        return self._access.put('phone/config/', dect_configuration)

    def start_dect_page(self):
        '''
        Starts dect paging
        '''
        return self._access.post('phone/dect_page_start/')

    def stop_dect_page(self):
        '''
        Stops dect paging
        '''
        return self._access.post('phone/dect_page_stop/')

    def start_fxs_ring(self):
        '''
        Rings
        '''
        return self._access.post('phone/fxs_ring_start/')

    def stop_fxs_ring(self):
        '''
        Stops ringing
        '''
        return self._access.post('phone/fxs_ring_stop/')
