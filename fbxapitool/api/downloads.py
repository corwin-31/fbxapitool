import urllib.parse
import base64

class Downloads:
    '''
    API to manage downloads
    '''

    def __init__(self, access):
        self._access = access

    task_priority = [ 'low', 'normal', 'high' ]
    task_status = [ 'stopped', 'queued', 'seeding', 'retry' ]
    task_write_parms = { 'queue_pos': 'int', 'io_priority': 'text', 'archive_password': 'text', 'status': 'text',
                        'info_hash': 'text', 'piece_length': 'int', 'stop_ratio': 'int' }
    task_configuration_schema = { 'queue_pos': 0, 'io_priority': task_priority[1], 'archive_password': '',
                                 'status': task_status[0], 'info_hash': '', 'piece_length': 262144 }
    throttling_modes = [ 'normal', 'slow', 'hibernate', 'schedule' ]
    throttling_write_parms = { throttling_modes[0]: 'sublist', throttling_modes[1]: 'sublist',
                              'schedule': 'list', 'mode': 'text' }
    throttling_configration_schema = { throttling_modes[0]: { 'rx_rate': 0, 'tx_rate': 0}, throttling_modes[1]: { 'rx_rate': 102400000, 'tx_rate': 51200000},
                                      'schedule': [], 'mode': throttling_modes[0] }
    feed_write_parms = { 'max_items': 'int', 'fetch_interval': 'int' }
    feed_configuration_schema = { 'max_items': 120, 'fetch_interval': 60 }
    news_write_parms = { 'user': 'text', 'password': 'text', 'erase_tmp': 'bool', 'port': 'int', 'nthreads': 'int',
                        'auto_repair': 'bool', 'ssl': 'bool', 'auto_extract': 'bool', 'lazy_par2': 'bool',
                        'server': 'text' }
    news_configuration_schema = { 'user': '', 'password': '', 'erase_tmp': True, 'port': 119, 'nthreads': 4,
                                 'auto_repair': True, 'ssl': False, 'auto_extract': True, 'lazy_par2': True,
                                 'server': 'news.free.fr' }
    crypto_supports = [ 'preferred', 'allowed', 'required', 'unsupported' ]
    bt_write_parms ={ 'enable_pex': 'bool', 'dht_port': 'int', 'announce_timeout': 'int', 'max_peers': 'int',
                     'main_port': 'int', 'enable_dht': 'bool', 'crypto_support': 'text', 'stop_ratio': 'int' }
    bt_configuration_schema ={ 'enable_pex': True, 'dht_port': 52239, 'announce_timeout': 30, 'max_peers': 50,
                              'main_port': 62811, 'enable_dht': True, 'crypto_support': crypto_supports[0],
                              'stop_ratio': 100 }
    blocklist_write_parms = { 'sources': 'list' }
    blocklist_configuration_schema = { 'sources': [] }
    global_write_parms = { 'use_watch_dir': 'bool', 'dns2': 'text', 'dns1': 'text', 'max_downloading_tasks': 'int',
                          'download_dir': 'text', 'watch_dir': 'text' }
    global_configuration_schema = { 'use_watch_dir': True, 'dns2': '0.0.0.0', 'dns1': '0.0.0.0',
                                   'max_downloading_tasks': 5, 'download_dir': 'L0ZyZWVib3gvVMOpbMOpY2hhcmdlbWVudHM=',
                                   'watch_dir': 'L0ZyZWVib3gvVMOpbMOpY2hhcmdlbWVudHMvQSBUw6lsw6ljaGFyZ2Vy' }
    full_configuration_schema = { 'use_watch_dir': True, 'dns2': '0.0.0.0', 'dns1': '0.0.0.0',
                                  'max_downloading_tasks': 5, 'download_dir': 'L0ZyZWVib3gvVMOpbMOpY2hhcmdlbWVudHM=',
                                  'watch_dir': 'L0ZyZWVib3gvVMOpbMOpY2hhcmdlbWVudHMvQSBUw6lsw6ljaGFyZ2Vy',
                                  'bt': bt_configuration_schema, 'news': news_configuration_schema,
                                  'feed': feed_configuration_schema, 'throttling': throttling_configration_schema,
                                  'blocklist': blocklist_configuration_schema }
    
    def get_config(self):
        '''
        Gets Download config
        '''
        return self._access.get('downloads/config/')

    def set_config(self, conf):
        '''
        Updates Download config
        '''
        return self._access.put('downloads/config/', conf)

    def get_stats(self):
        '''
        Gets Download stats
        '''
        return self._access.get('downloads/stats')

    def set_throttling(self, mode='normal'):
        '''
        Updates Download throttling mode (normal, slow, hibernate or schedule)
        '''
        return self._access.put('downloads/throttling', { 'throttling': mode })

    def get_tasks(self):
        '''
        Gets Download tasks
        '''
        return self._access.get('downloads/')

    def get_task(self, id):
        '''
        Gets a Download task
        '''
        return self._access.get(f"downloads/{id}")

    def get_task_log(self, id):
        '''
        Gets log of a Download task
        '''
        return self._access.get(f"downloads/{id}/log")

    def del_task(self, id, erase=False):
        '''
        Deletes a Download task
        '''
        if erase: return self._access.delete(f"downloads/{id}/erase")
        else: return self._access.delete(f"downloads/{id}")

    def set_task(self, id, conf):
        '''
        Updates Download task
        '''
        return self._access.put(f"downloads/{id}", conf)

    def add_task(self, url):
        '''
        Adds a Download task : single already encoded url without option
        '''
        return self._access.post('downloads/add', payload = f"download_url={url}", raw=True)

    def add_full(self, url, ddir=None, target=None, hsh=None, rec=False):
        '''
        Adds a Download task : single url without option + download parms
        '''
        # Encode url with all parms before submitting
        pload = 'download_url=' + urllib.parse.quote(url, safe='')
        if ddir != None: pload = pload + '&download_dir=' + base64.b64encode(ddir.encode('utf-8')).decode('utf-8')
        if target != None: pload = pload + '&filename=' + target
        if hsh != None: pload + '&hash=' + urllib.parse.quote(hsh, safe='')
        if rec: pload = pload + '&recursive=True'
        return self._access.post('downloads/add', payload = pload, raw=True)

    def get_task_files(self, id):
        '''
        Gets list of files for a Download task
        '''
        return self._access.get(f"downloads/{id}/files")

    def set_file_priority(self, task_id, file_id, priority='normal'):
        '''
        Updates a Download task priority (no_dl, low, normal, high)
        '''
        return self._access.put(f"downloads/{task_id}/files/{file_id}", { 'priority': priority })

    def get_task_trackers(self, id):
        '''
        Gets trackers of a Download task
        '''
        return self._access.get(f"downloads/{id}/trackers")

    def add_task_tracker(self, id,  url):
        '''
        Adds a tracker to a Download task : signle url without option
        '''
        return self._access.post(f"downloads/{id}/trackers", { 'announce': url })

    def del_task_tracker(self, id, url):
        '''
        Deletes a tracker for a Download task
        '''
        announce = urllib.parse.quote(url, safe='')
        return self._access.delete(f"downloads/{id}/trackers/{announce}", { 'announce': url })

    def start_task_tracker(self, id, url):
        '''
        Starts a tracker for a Download task
        '''
        announce = urllib.parse.quote(url, safe='')
        return self._access.put(f"downloads/{id}/trackers/{announce}", { 'announce': url, 'is_enabled' : True })

    def stop_task_tracker(self, id, url):
        '''
        Stops a tracker for a Download task
        '''
        announce = urllib.parse.quote(url, safe='')
        return self._access.put(f"downloads/{id}/trackers/{announce}", { 'announce': url, 'is_enabled' : False })

    def get_task_peers(self, id):
        '''
        Gets peers of a Download task
        '''
        return self._access.get(f"downloads/{id}/peers")

    def get_task_pieces(self, id):
        '''
        Gets pieces of a Download task
        '''
        return self._access.get(f"downloads/{id}/pieces")

    def get_task_blacklist(self, id):
        '''
        Gets blacklist of a Download task
        '''
        return self._access.get(f"downloads/{id}/blacklist")

    def del_task_blacklist(self, id):
        '''
        Deletes blacklist for a Download task
        '''
        return self._access.delete(f"downloads/{id}/blacklist/empty")

    def del_task_blackentry(self, id, host):
        '''
        Deletes blacklist entry for a Download task
        '''
        return self._access.delete(f"downloads/{id}/blacklist/{host}")

    def add_task_blackentry(self, id, host):
        '''
        Adds an entry in the blacklist of a Download task
        '''
        return self._access.post(f"downloads/{id}/blacklist", { 'host': host, 'expire': 3600 })

    def get_rssfeeds(self):
        '''
        Gets RSS feeds
        '''
        return self._access.get('downloads/feeds/')

    def get_rssfeed(self, id):
        '''
        Gets a RSS feeds
        '''
        return self._access.get(f"downloads/feeds/{id}")

    def add_rssfeed(self, url):
        '''
        Adds rss feed
        '''
        return self._access.post('downloads/feeds/', { 'url': url })

    def del_rssfeed(self, id):
        '''
        Deletes a rss feed
        '''
        return self._access.delete(f"downloads/feeds/{id}")

    def set_rssfeed_mode(self, id, mode=True):
        '''
        Sets mode auto_download to a rss feed
        '''
        return self._access.put(f"downloads/feeds/{id}", { 'auto_download': mode })

    def refresh_rssfeed(self, id):
        '''
        Refreshes a rss feed
        '''
        return self._access.post(f"downloads/feeds/{id}/fetch")

    def refresh_rssfeeds(self):
        '''
        Refreshes all rss feeds
        '''
        return self._access.post('downloads/feeds/fetch')

    def get_rssfeed_items(self, id):
        '''
        Gets RSS feed items
        '''
        return self._access.get(f"downloads/feeds/{id}/items/")

    def mark_rssfeed_item(self, feed_id, item_id, as_read=True):
        '''
        Marks or unmarks a RSS feed item as read
        '''
        return self._access.put('downloads/feeds/{feed_id}/items/{item_id}', { 'is_read': as_read })

    def set_rssfeed_download_item(self, feed_id, item_id):
        '''
        Enqueues the download of a RSS feed item
        '''
        return self._access.post('downloads/feeds/{feed_id}/items/{item_id}/download')

    def set_rssfeed_mark_all_items_as_read(self, id):
        '''
        Marks all items as read for a RSS feed
        '''
        return self._access.post('downloads/feeds/{id}/items/mark_all_as_read')
