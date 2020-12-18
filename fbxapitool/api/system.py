class System:
    '''
    API of basic system functions
    '''

    def __init__(self, access):
        self._access = access

    def get_config(self):
        '''
        Gets system configuration:
        '''
        return self._access.get('system/')


    def reboot(self):
        '''
        Reboots freebox
        '''
        return self._access.post('system/reboot')
