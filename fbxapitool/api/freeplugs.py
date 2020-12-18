class Freeplugs:
    '''
    API for using CPL freeplugs
    '''

    def __init__(self, access):
        self._access = access

    def get_freeplugs_list(self):
        '''
        Gets freeplug list
        '''
        return self._access.get('freeplug/')

    def get_freeplug(self, fp_id):
        '''
        Gets freeplug #fp_id
        '''
        return self._access.get('freeplug/{0}/'.format(fp_id))

    def reset_freeplug(self, fp_id):
        '''
        Resets freeplug #fp_id
        '''
        return self._access.post(f'freeplug/{fp_id}/reset/')
