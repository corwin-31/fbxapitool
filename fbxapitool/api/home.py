class Home:
    '''
    API for Home Automation
    Warning : not tested
    '''

    def __init__(self, access):
        self._access = access

    home_endpoint_value_schema = { 'value': None }
    create_home_node_rule_payload_schema = { 'iconUrl': '', 'id': 0, 'label': '', 'name': '',
        'role': 0, 'roleLabel': '', 'type': '' }
    node_rule_role_schema = { 'node': [ 0 ], 'role': 0 }
    node_rule_configuration_data_schema = { 'roles': [ node_rule_role_schema ] }
    sms_number_data_schema = { 'description': 'Mon numero', 'phoneNumber': '',
        'smsEnabled': True, 'voicemailEnabled': True }
    sms_validation_data_schema = { 'applicationHash': '' }
    sms_number_validation_data_schema = { 'validationCode': '' }
    next_pairing_step_payload_schema = { 'session': 0, 'pageid': 0, 'fields': [None] }
    start_pairing_step_payload_schema = { 'nfc': True, 'qrcode': False, 'type': '' }
    stop_pairing_step_payload_schema = { 'session': 0 }

    def del_home_adapter(self, home_adapter_id):
        '''
        Deletes home adapter
        '''
        return self._access.delete(f'home/adapters/{home_adapter_id}')

    def get_home_adapter(self, home_adapter_id):
        '''
        gets a registered home adapter
        '''
        return self._access.get(f'home/adapters/{home_adapter_id}')

    def get_home_adapters(self):
        '''
        Gets the list of registered home adapters
        '''
        return self._access.get('home/adapters')

    def get_camera(self):
        '''
        Gets camera info
        '''
        return self._access.get('camera')

    def get_camera_snapshot(self, camera_index=0, size=4, quality=5):
        '''
        Gets a camera snapshot
        size: 2 = 320x240, 3 = 640x480, 4 = 1280x720
        '''
        fbx_cameras = self.get_camera()
        return self._access.get(fbx_cameras[camera_index]['stream_url'].replace('stream.m3u8', f'snapshot.cgi?size={size}&quality={quality}')[1:])

    def get_camera_stream_m3u8(self, camera_index=0, channel=2):
        '''
        Gets camera stream
        channel: 1 is SD, 2 is HD
        '''
        fbx_cameras = self.get_camera()
        return self._access.get(fbx_cameras[camera_index]['stream_url'].replace('stream.m3u8', f'stream.m3u8?channel={channel}')[1:])

    def get_camera_ts(self, ts_name, camera_index=0):
        '''
        Gets camera stream
        '''
        fbx_cameras = self.get_camera()
        return self._access.get(fbx_cameras[camera_index]['stream_url'].replace('stream.m3u8', f'{ts_name}')[1:])

    def get_home_endpoint_value(self, node_id, endpoint_id):
        '''
        Gets home endpoint value
        '''
        return self._access.get(f'home/endpoints/{node_id}/{endpoint_id}')

    def get_home_endpoint_values(self, endpoint_list):
        '''
        Gets home endpoint values
        '''
        return self._access.post('home/endpoints/get', endpoint_list)

    def set_home_endpoint_value(self, node_id, endpoint_id, home_endpoint_value):
        '''
        Sets home endpoint value
        '''
        return self._access.put(f'home/endpoints/{node_id}/{endpoint_id}', home_endpoint_value)

    def del_home_link(self, link_id):
        '''
        Deletes home link
        '''
        return self._access.delete(f'home/links/{link_id}')

    def get_home_link(self, link_id):
        '''
        Gets home link
        '''
        return self._access.get(f'home/links/{link_id}')

    def get_home_links(self):
        '''
        Gets home links
        '''
        return self._access.get('home/links')

    def del_home_node(self, node_id):
        '''
        Deletes home node id
        '''
        return self._access.delete(f'home/nodes/{node_id}')

    def get_home_node(self, node_id):
        '''
        Gets home node #node_id
        '''
        return self._access.get(f'home/nodes/{node_id}')

    def edit_home_node(self, node_id, node_data):
        '''
        Edits home node data
        '''
        return self._access.put(f'home/nodes/{node_id}', node_data)

    def get_home_nodes(self):
        '''
        Gets home nodes
        '''
        return self._access.get('home/nodes')

    def create_home_node_rule(self, template_name, create_home_node_rule_payload):
        '''
        Creates home node rule
        '''
        return self._access.post(f'home/rules/{template_name}', create_home_node_rule_payload)

    def get_home_node_existing_rule_config(self, node_id, rule_node_id, role_id):
        '''
        Gets home node existing rule configuration data
        '''
        return self._access.get(f'home/nodes/{node_id}/rules/node/{rule_node_id}/{role_id}')

    def get_home_node_template_rule_config(self, node_id, template_name, role_id):
        '''
        Gets node rule template configuration data
        '''
        return self._access.get(f'home/nodes/{node_id}/rules/template/{template_name}/{role_id}')

    def set_home_node_rule_config(self, rule_node_id, node_rule_configuration_data):
        '''
        Sets node rule configuration data
        '''
        return self._access.put(f'home/rules/{rule_node_id}', node_rule_configuration_data)

    def get_home_node_new_rules(self, node_id):
        '''
        Gets node new rules
        '''
        return self._access.get(f'home/nodes/{node_id}/rules')

    def get_secmod(self):
        '''
        Gets security module
        '''
        return self._access.get('home/secmod')

    def create_sms_number(self, sms_number_data):
        '''
        Creates sms number
        '''
        return self._access.post('home/sms/numbers', sms_number_data)

    def edit_sms_number(self, sms_number_id, sms_number_data):
        '''
        Edits sms number
        '''
        return self._access.put(f'home/sms/numbers/{sms_number_id}', sms_number_data)

    def get_sms_numbers(self):
        '''
        Gets sms numbers
        '''
        return self._access.get('home/sms/numbers')

    def send_sms_number_validation(self, sms_number_id, sms_validation_data):
        '''
        Sends sms number validation
        '''
        return self._access.post(f'home/sms/numbers/{sms_number_id}/send_validation_sms', sms_validation_data)

    def validate_sms_number(self, sms_number_id, sms_number_validation_data):
        '''
        Validates sms number
        '''
        return self._access.post(f'home/sms/numbers/{sms_number_id}/validate', sms_number_validation_data)

    def get_home_tile(self, tile_id):
        '''
        Gets the home tile with provided id
        '''
        return self._access.get(f'home/tileset/{tile_id}')

    def get_home_tilesets(self):
        '''
        Gets the list of home tileset
        '''
        return self._access.get('home/tileset/all')

    def get_home_pairing_state(self, home_adapter_id):
        '''
        Gets the current home pairing state
        '''
        return self._access.get(f'home/pairing/{home_adapter_id}')

    def next_home_pairing_step(self, home_adapter_id, next_pairing_step_payload):
        '''
        Next home pairing step
        '''
        return self._access.post(f'home/pairing/{home_adapter_id}', next_pairing_step_payload)

    def start_home_pairing_step(self, home_adapter_id, start_pairing_step_payload):
        '''
        Starts home pairing step
        '''
        return self._access.post(f'home/pairing/{home_adapter_id}', start_pairing_step_payload)

    def stop_home_pairing_step(self, home_adapter_id, stop_pairing_step_payload):
        '''
        Stops home pairing
        '''
        return self._access.post(f'home/pairing/{home_adapter_id}', stop_pairing_step_payload)
