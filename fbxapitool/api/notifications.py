class Notifications:
    '''
    API to manage notifications
    Warning : partially tested
    '''

    def __init__(self, access):
        self._access = access

    os_type = [ 'android', 'ios' ]
    subscription = [ 'security', 'wan', 'downloader', 'phone' ]
    notification_target_data_schema = { 'id': '', 'name': '', 'subscriptions': subscription,
        'token': '', 'type': os_type[0] }

    def create_notification_target(self, notification_target_data=notification_target_data_schema):
        '''
        Creates notification target
        '''
        return self._access.post('notif/targets/', notification_target_data)

    def delete_notification_target(self, target_id):
        '''
        Deletes notification target
        '''
        return self._access.delete(f"notif/targets/{target_id}")

    def edit_notification_target(self, target_id, notification_target_data):
        '''
        Edits notification target
        '''
        return self._access.put(f"notif/targets/{target_id}", notification_target_data)

    def get_notification_target(self, target_id):
        '''
        Gets notification target
        '''
        return self._access.get(f"notif/targets/{target_id}")

    def get_notification_targets(self):
        '''
        Gets notification targets
        '''
        return self._access.get('notif/targets/')
