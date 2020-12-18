import base64
import os
import logging

logger = logging.getLogger(__name__)

class Fs:
    '''
    API for navigation into freebox file system
    '''

    def __init__(self, access):
        self._access = access
        self._path = '/'

    archive_schema = { 'dst': '', 'files': [ '' ] }
    conflict_mode = [ 'overwrite', 'both', 'recent', 'skip' ]
    cpmv_schema = { 'dst': '', 'files': [ '' ], 'mode': conflict_mode[0] }
    mkdir_schema = { 'dirname': '', 'parent': '' }
    mkpath_schema = { 'path': '' }
    extractrename_schema = { 'src': '', 'dst': '' }
    hash_file_schema = { 'src': '', 'hash_type': 'sha1' }
    rm_schema = { 'files': [ '' ] }
    task_states = [ 'queued', 'running', 'paused', 'done', 'failed' ]
    update_task_state_schema = { 'state': task_states[0] }

    def pwd(self):
        '''
        Gets working directory
        '''
        return self._path

    def cd(self, path):
        '''
        Changes working directory
        '''
        if self._path_exists(path):
            self._path = os.path.join(self._path, path)
        else:
            logger.error('{0} does not exist'.format(os.path.join(self._path, path)))

    def _path_exists(self, path):
        '''
        Checks if path exists
        '''
        try:
            self.get_file_info(os.path.join(self._path, path))
            return True
        except:
            return False

    def ls(self):
        '''
        Lists directory
        '''
        return [i["name"] for i in self.list_files(self._path)]

    def mkdir(self, create_directory=create_directory_schema):
        '''
        Creates directory
        '''
        return self._access.post("fs/mkdir/", create_directory)

    def mkpath(self, path):
        '''
        Creates path
        '''
        self.create_path_schema["path"] = base64.b64encode(path.encode("utf-8")).decode("utf-8")
        return self._access.post("fs/mkpath/", self.create_path_schema)

    def list_files(self, path, remove_hidden=0, count_sub_folder=0):
        '''
        Returns the list of files for the given path
        '''
        path_b64 = base64.b64encode(path.encode('utf-8')).decode('utf-8')
        return self._access.get(f"fs/ls/{path_b64}?removeHidden={1 if remove_hidden else 0}&countSubFolder={1 if count_sub_folder else 0}")

    def get_file_info(self, path):
        '''
        Returns informations for the given path
        '''
        path_b64 = base64.b64encode(path.encode('utf-8')).decode('utf-8')
        return self._access.get('fs/ls/{0}'.format(path_b64))

    def rename_file(self, src, dst):
        '''
        Renames file src (with its path) to dst (new file name)
        '''
        self.rename_schema["src"] = base64.b64encode(src.encode("utf-8")).decode("utf-8")
        self.rename_schema["dst"] = dst
        return self._access.post("fs/rename/", self.rename_schema)

    def mv(self, move):
        '''
        Moves files
        '''
        return self._access.post("fs/mv/", move)

    def cp(self, copy):
        '''
        Copy files
        '''
        return self._access.post("fs/copy/", copy)

    def rm(self, remove):
        '''
        Deletes files
        '''
        return self._access.post("fs/rm/", remove)

    def hash_file(self, src, hash_type):
        '''
        Hash a file src (with its path), hash_type = type of hash (md5, sha1, ...)
        '''
        self.hash_file_schema["src"] = base64.b64encode(src.encode("utf-8")).decode("utf-8")
        self.hash_file_schema["hash_type"] = hash_type
        return self._access.post("fs/hash/", self.hash_file_schema)

    def get_hash(self, id):
        '''
        Gets the hash value : task #id must have succeed and also be in state "done"
        '''
        return self._access.get(f"fs/tasks/{id}/hash")

    def archive_files(self, archive):
        '''
        Archives files
        '''
        return self._access.post("fs/archive/", archive)

    def extract_archive(self, extract):
        '''
        Extracts archive
        '''
        return self._access.post("fs/extract/", extract)

    def get_tasks_list(self):
        '''
        Return the collection of all tasks
        '''
        return self._access.get('fs/tasks/')

    def delete_file_task(self, id):
        '''
        Deletes file task
        '''
        return self._access.delete(f"fs/tasks/{id}")

    def set_file_task_state(self, id, update_task_state):
        '''
        Sets file task state
        '''
        return self._access.put(f"fs/tasks/{id}", update_task_state)
