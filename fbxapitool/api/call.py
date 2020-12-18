class Call:
    '''
    API to manage phone calls
    '''

    def __init__(self, access):
        self._access = access

    mark_call_log_as_read_data_schema = { "new": False }

    def get_call_list(self):
        '''
        Returns the collection of all calls
        '''
        return self._access.get('call/log/')

    def get_call(self, id):
        '''
        Gets call #id
        '''
        return self._access.get('call/log/{0}'.format(id))
    
    def mark_call_list_as_read(self):
        '''
        Marks all calls as read
        '''
        return self._access.post('call/log/mark_all_as_read')

    def mark_call_as_read(self, id):
        '''
        Marks call #id as read
        '''
        return self._access.put('call/log/{0}'.format(id), payload=self.mark_call_log_as_read_data_schema)

    def delete_call_list(self):
        '''
        Deletes all calls
        '''
        return self._access.post('call/log/delete_all/')

    def delete_call(self, id):
        '''
        Deletes call #id
        '''
        return self._access.delete('call/log/{0}'.format(id))
