import time

class Tv:
    '''
    API for TV functions
    Warning : not tested
    '''

    def __init__(self, access):
        self._access = access

    def archive_tv_record(self, record_id):
        '''
        Archives tv record
        '''
        return self._access.post(f'pvr/programmed/{record_id}/ack/')

    def create_tv_record(self, tv_record):
        '''
        Creates tv record
        '''
        return self._access.post('pvr/programmed/', tv_record)

    def create_tv_record_generator(self, tv_record_generator):
        '''
        Creates tv record generator
        '''
        return self._access.post('pvr/generator/', tv_record_generator)

    def delete_finished_tv_record(self, record_id):
        '''
        Deletes finished tv record
        '''
        return self._access.delete(f'pvr/finished/{record_id}')

    def delete_planned_tv_record(self, record_id):
        '''
        Deletes planned tv record
        '''
        return self._access.delete(f'pvr/programmed/{record_id}')

    def delete_tv_record_generator(self, generator_id):
        '''
        Deletes tv record generator
        '''
        return self._access.delete(f'pvr/generator/{generator_id}')

    def edit_finished_tv_record(self, record_id, finished):
        '''
        Edits finished tv record
        '''
        return self._access.put(f'pvr/finished/{record_id}', finished)

    def edit_planned_tv_record(self, record_id, tv_record):
        '''
        Edits planned tv record
        '''
        return self._access.put(f'pvr/programmed/{record_id}', tv_record)

    def edit_tv_record_generator(self, generator_id, tv_record_generator):
        '''
        Edits tv record generator
        '''
        return self._access.put(f'pvr/generator/{generator_id}', tv_record_generator)

    def get_finished_tv_records(self):
        '''
        Gets finished tv records
        '''
        return self._access.get('pvr/finished/')

    def get_mycanal_token(self):
        '''
        Gets mycanal token
        '''
        return self._access.get('tv/mycanal_token')

    def get_planned_tv_records(self):
        '''
        Gets planned tv records
        '''
        return self._access.get('pvr/programmed/')

    def get_tv_bouquet(self):
        '''
        Gets tv bouquet
        '''
        return self._access.get('tv/bouquets/')

    def get_tv_bouquet_channels(self, bouquet_id='freeboxtv'):
        '''
        Gets tv bouquet channels
        '''
        return self._access.get(f'tv/bouquets/{bouquet_id}/channels/')

    def get_tv_channels(self):
        '''
        Gets tv channels
        '''
        return self._access.get('tv/channels/')

    def get_tv_default_bouquet_channels(self):
        '''
        Gets tv default bouquet channels
        '''
        return self.get_tv_bouquet_channels()

    def get_tv_program(self, program_id):
        '''
        Gets tv program
        '''
        return self._access.get(f'tv/epg/programs/{program_id}')

    def get_tv_program_highlights(self, channel_id, date=int(time.time())):
        '''
        Gets tv program highlights
        '''
        return self._access.get(f'tv/epg/highlights/{channel_id}/{date}')

    def get_tv_programs_by_channel(self, channel_id, date=int(time.time())):
        '''
        Gets tv programs by channel
        '''
        return self._access.get(f'tv/epg/by_channel/{channel_id}/{date}')

    def get_tv_programs_by_date(self, date=int(time.time())):
        '''
        Gets tv programs by date
        '''
        return self._access.get(f'tv/epg/by_time/{date}')

    def get_tv_records_configuration(self):
        '''
        Gets tv records configuration
        '''
        return self._access.get('pvr/config/')

    def get_tv_record_generator(self, generator_id):
        '''
        Gets tv record generator
        '''
        return self._access.get(f'pvr/generator/{generator_id}')

    def get_tv_records_media_list(self):
        '''
        Gets tv records media list
        '''
        return self._access.get('pvr/media/')

    def get_tv_status(self):
        '''
        Gets tv status
        '''
        return self._access.get('tv/status/')
