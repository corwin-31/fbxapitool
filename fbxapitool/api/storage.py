class Storage:
    '''
    API to manages storage & external disks connected to the box
    '''

    def __init__(self, access):
        self._access = access

    eject_disk_schema = { 'state': 'disabled' }
    mount_disk_schema = { 'state': 'enabled' }
    format_fs_types = [ 'vfat', 'exfat', 'xfs', 'ext4', 'ntf', 'hf', 'hfsplus', 'swap' ]
    format_table_types = [ 'msdos', 'gpt', 'superfloppy' ]
    format_schema = { 'label': '', 'fs_type': 'vfat', 'table_type': 'msdos' }
    check_modes = [ 'ro', 'rw' ]
    mount_partition_schema = { 'state': 'mounted' }
    umount_partition_schema = { 'state': 'umounted' }

    def check_partition(self, id, fix=False):
        '''
        Checks partition #id
        '''
        if fix: check_type = { 'checkmode': self.check_modes[1] }
        else: check_type = { 'checkmode': self.check_modes[0] }
        return self._access.put(f"storage/partition/{id}/check", check_type)

    def umount_partition(self, part_id):
        '''
        Unmounts partition
        '''
        return self._access.put(f"storage/partition/{part_id}", self.umount_partition_schema)

    def mount_partition(self, part_id):
        '''
        Mounts partition
        '''
        return self._access.put(f"storage/partition/{part_id}", self.mount_partition_schema)

    def eject_disk(self, disk_id):
        '''
        Ejects storage disk
        '''
        return self._access.put(f"storage/disk/{disk_id}", self.eject_disk_schema)

    def mount_disk(self, disk_id):
        '''
        Mounts storage disk
        '''
        return self._access.put(f"storage/disk/{disk_id}", self.mount_disk_schema)

    def format_disk(self, id, label='', fs='vfat', table='msdos'):
        '''
        Formats partition
        '''
        format_data = { 'label': label, 'fs_type': fs, 'table_type': table }
        return self._access.put(f"storage/disk/{id}/format", format_data)

    def get_config(self):
        '''
        Gets storage configuration
        '''
        return self._access.get("storage/config/")

    def get_disk(self, id):
        '''
        Gets disk #id
        '''
        return self._access.get(f"storage/disk/{id}")

    def get_disks(self):
        '''
        Gets disks list
        '''
        return self._access.get("storage/disk/")

    def get_partition(self, id):
        '''
        Gets partition #id
        '''
        return self._access.get(f"storage/partition/{id}")

    def get_partitions(self):
        '''
        Gets partitions list
        '''
        return self._access.get("storage/partition/")

    def get_raid(self, id):
        '''
        Gets raid
        '''
        return self._access.get(f"storage/raid/{id}")

    def get_raids(self):
        '''
        Gets raids list
        '''
        return self._access.get("storage/raid/")

    def get_media_list(self):
        '''
        Gets storage media list
        '''
        return self._access.get('pvr/media/')
