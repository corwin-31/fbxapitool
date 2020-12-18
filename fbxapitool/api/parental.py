class Parental:
    '''
    API to manage Parental control
    Warning : obsolete, for old non up-to-date or migrated freebox
    Warning : not tested
    '''
    def __init__(self, access):
        self._access = access
    
    filter_modes = [ 'allowed', 'denied', 'webonly' ]
    default_filter_mode = filter_modes[0]
    parental_control_configuration_schema = { 'default_filter_mode': default_filter_mode }

    def create_parental_filter(self, parental_filter):
        '''
        Creates parental filter
        '''
        return self._access.post('parental/filter/', parental_filter)

    def delete_parental_filter(self, filter_id):
        '''
        Deletes parental filter
        '''
        return self._access.delete(f"parental/filter/{filter_id}")

    def edit_parental_filter(self, filter_id, parental_filter):
        '''
        Edits parental filter
        '''
        return self._access.put(f"parental/filter/{filter_id}", parental_filter)

    def edit_parental_filter_planning(self, filter_id, parental_filter_planning):
        '''
        Edits parental filter planning
        '''
        return self._access.put(f"parental/filter/{filter_id}/planning/", parental_filter_planning)

    def get_parental_config(self):
        '''
        Gets parental config
        '''
        return self._access.get('parental/config/')

    def get_parental_filter_planning(self, filter_id):
        '''
        Gets parental filter planning
        '''
        return self._access.get(f"parental/filter/{filter_id}/planning/")

    def get_parental_filters(self):
        '''
        Gets parental filters
        '''
        return self._access.get('parental/filter/')

    def set_parental_control_configuration(self, parental_control_configuration=parental_control_configuration_schema):
        '''
        Sets parental control configuration
        '''
        return self._access.put('parental/config/', parental_control_configuration)

class Profile:
    '''
    (The new) API to manage network profiles
    '''
    def __init__(self, access):
        self._access = access

    profile_write_parms = { 'name': 'text', 'icon': 'text' }
    profile_data_schema = { 'name': '', 'icon': '/resources/images/profile/profile_01.png' }
    netcontrol_modes = [ 'allowed', 'denied', 'webonly' ]
    cday_values = [ ':fr_bank_holidays', ':fr_school_holidays_a', ':fr_school_holidays_b', ':fr_school_holidays_c', ':fr_school_holidays_corse' ]
    netcontrol_write_parms = { 'override_mode': 'text', 'macs': 'list', 'cdayranges': 'list' }
    netcontrol_data_schema = { 'override_mode': netcontrol_modes[2], 'macs': [], 'cdayranges': [] }
    rule_write_parms = { 'name': 'text', 'mode': 'text', 'start_time': 'int', 'end_time': 'int', 'enabled': 'bool', 'weekdays': 'list' }
    rule_data_schema = { 'name': '', 'mode': netcontrol_modes[1], 'start_time': 0, 'end_time': 0, 'enabled': True, 'weekdays': [] }
    
    def get_profiles(self):
        '''
        Gets all profiles
        '''
        return self._access.get('profile/')

    def get_profile(self, profile_id):
        '''
        Gets all profiles
        '''
        return self._access.get(f"profile/{profile_id}")

    def add_profile(self, new_profile):
        '''
        Adds a profile
        '''
        return self._access.post('profile/', new_profile)

    def del_profile(self, profile_id):
        '''
        Deletes a profile
        '''
        return self._access.delete(f"profile/{profile_id}")

    def set_profile(self, profile_id, data):
        '''
        Configures a profile
        '''
        return self._access.put(f"profile/{profile_id}", payload=data)

    def get_netcontrols(self):
        '''
        Gets network control for all profiles
        '''
        return self._access.get('network_control/')

    def get_netcontrol(self, profile_id):
        '''
        Gets network control for a profile
        '''
        return self._access.get(f"network_control/{profile_id}")

    def set_netcontrol(self, profile_id, data):
        '''
        Sets network control for a profile
        '''
        return self._access.put(f"network_control/{profile_id}", payload=data)
    
    def override(self, profile_id, duration=0):
        '''
        Switch to override mode for the specified duration
        '''
        oldconf = self.get_netcontrol(profile_id)
        return self._access.put(f"network_control/{profile_id}", { 'override': True, 'override_until': duration, 'macs': oldconf['macs'] })

    def back(self, profile_id):
        '''
        Switch to standard mode
        '''
        oldconf = self.get_netcontrol(profile_id)
        return self._access.put(f"network_control/{profile_id}", { 'override': False, 'macs': oldconf['macs'] })

    def get_migration_status(self):
        '''
        Gets migration status
        '''
        return self._access.get('network_control/migrate')

    def migrate(self):
        '''
        Migrates to new version
        '''
        return self._access.post('network_control/migrate', payload=None)

    def get_netcontrol_rules(self, profile_id):
        '''
        Gets all rules for a network control profile
        '''
        return self._access.get(f"network_control/{profile_id}/rules/")

    def get_netcontrol_rule(self, profile_id, rule_id):
        '''
        Gets a rule for a network control profile
        '''
        return self._access.get(f"network_control/{profile_id}/rules/{rule_id}")

    def add_netcontrol_rule(self, profile_id, new_profile):
        '''
        Adds a rule for a network control profile
        '''
        if 'weekdays' in new_profile:
            newlist = []
            for day in new_profile['weekdays']: newlist.append(day == 'True')
            new_profile['weekdays'] = newlist
        return self._access.post(f"network_control/{profile_id}/rules/", new_profile)

    def set_netcontrol_rule(self, profile_id, rule_id, data):
        '''
        Sets a rule for a network control profile
        '''
        if 'weekdays' in data:
            newlist = []
            for day in data['weekdays']: newlist.append(day == 'True')
            data['weekdays'] = newlist
        return self._access.put(f"network_control/{profile_id}/rules/{rule_id}", data)

    def del_netcontrol_rule(self, profile_id, rule_id):
        '''
        Deletes a profile
        '''
        return self._access.delete(f"network_control/{profile_id}/rules/{rule_id}")
