class Contact:
    '''
    API to manage contacts, partially implemented : missing photo, url, addresses, emails
    '''

    def __init__(self, access):
        self._access = access
        
    contact_write_parms = {'display_name': 'text', 'first_name': 'text', 'last_name': 'text', 'company': 'text' }
    contact_write_numbers = { 'number': 'text', 'type': 'text', 'is_default': 'bool' }
    contact_number_type = [ 'fixed', 'mobile', 'work', 'fax', 'other' ]
    contact_number_schema = { 'number': '0', 'type': contact_number_type[0], 'contact_id': 0, 'is_default': False }
    contact_configuration_schema = { 'display_name': 'Batman', 'first_name': 'Bruce', 'last_name': 'Wayne','company': 'DC Comics' }

    def get_contact_list(self):
        '''
        Returns the collection of all contact entries
        '''
        return self._access.get('contact/')

    def get_contact(self, id):
        '''
        Gets contact #id
        '''
        return self._access.get('contact/{0}'.format(id))

    def add_contact(self, conf):
        '''
        Adds a contact
        '''
        return self._access.post('contact/', payload=conf)

    def del_contact(self, id):
        '''
        Removes a contact
        '''
        return self._access.delete('contact/{0}'.format(id))

    def update_contact(self, id, conf):
        '''
        Updates a contact
        '''
        return self._access.put('contact/{0}'.format(id), payload=conf)
    
    def add_number(self, id, conf):
        '''
        Adds a number for a contact
        '''
        conf['contact_id'] = id
        return self._access.post('number/', payload=conf)
    
    def del_number(self, id):
        '''
        Deletes a number
        '''
        return self._access.delete('number/{0}'.format(id))
    
    def update_number(self, id, conf):
        '''
        Updates a number
        '''
        return self._access.put('number/{0}'.format(id), payload=conf)
