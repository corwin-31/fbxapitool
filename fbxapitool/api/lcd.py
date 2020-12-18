class Lcd:
    '''
    API to configure LCD display on the box
    '''

    def __init__(self, access):
        self._access = access

    lcd_write_parms = { 'brightness': 'int' } # Delta
    lcd_config_schema = { 'orientation': 0, 'brightness': 100, 'orientation_forced': False }

    def get_configuration(self):
        '''
        Gets configuration
        '''
        return self._access.get('lcd/config')

    def set_configuration(self, lcd_config=None):
        '''
        Sets configuration
        '''
        if lcd_config is None:
            lcd_config = self.lcd_config_schema
        return self._access.put('lcd/config', lcd_config)
