#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Displays a summary of status informations
'''
from fbxapitool import Freebox
import time
import locale
import base64

locale.setlocale(locale.LC_ALL, str('fr_FR.UTF-8'))
    
# Instantiate Freebox class and connect to freebox
fbx = Freebox()
fbx.open('mafreebox.freebox.fr',443)

print('______________________________________________________________________')
print('')
print('                      Etat de la Freebox')
print('______________________________________________________________________')
print('')
print('Informations générales :')
print('========================')
print('')

# Get main data
fbx_config = fbx.system.get_config()
fbx_connection_status_details = fbx.connection.get_status_details()
fbx_connection_logs = fbx.connection.get_logs()
fbx_connection_config = fbx.connection.get_config()
fbx_ipv6 = fbx.connection.get_ipv6_config()
fbx_dhcp_config = fbx.dhcp.get_config()
fbx_phone = fbx.phone.get_list()
fbx_wifi = fbx.wifi.get_global_config()
fbx_wifi_ap = fbx.wifi.get_ap_list()
fbx_bss = fbx.wifi.get_bss_list()
lan_config = fbx.lan.get_config()
dmz_config = fbx.fw.get_dmz_config()
fbx_static_dhcp = fbx.dhcp.get_static_dhcp_lease()
fbx_dyn_dhcp = fbx.dhcp.get_dynamic_dhcp_lease()
fbx_ports = fbx.fw.get_forward()
fbx_switch_status = fbx.switch.get_status()
fbx_media = fbx.airmedia.get_config()
fbx_freeplugs = fbx.freeplugs.get_freeplugs_list()

print('  Modèle                         {0}'.format(fbx_config['board_name']))
print('  Nom du modèle                  {0}'.format(fbx_config['model_info']['pretty_name']))
print('  Version du firmware            {0}'.format(fbx_config['firmware_version']))
print('  N° de série                    {0}'.format(fbx_config['serial']))
print('  Mode de connection             {0}'.format(fbx_connection_status_details['media'].upper()))
status = fbx_connection_status_details['state']
if status == 'up':
    status_str = 'Ok'
elif status == 'down':
    status_str = 'Off'
elif status == 'going_up':
    status_str = 'Initialisation'
elif status == 'going_down':
    status_str = 'En cours de fermeture'
else :
    status_str = 'Inconnue'
print('  Etat de la connection          {0}'.format(status_str))
if fbx_config['box_authenticated'] == True:
    auth = 'Ok'
else :
    auth = 'Non'
print('  Etat de l\'authentification     {0}'.format(auth))
status = fbx_config['disk_status']
if status == 'active':
    status_str = 'Actif'
else :
    status_str = 'Inactif'
print('  Statut du disque               {0}'.format(status_str))
if status == 'active': print('  Stockage principal             {0}'.format(fbx_config['user_main_storage']))
print('  Temps depuis la mise en route  {0}'.format(fbx_config['uptime']))
bytes_down = fbx_connection_status_details['bytes_down']
bytes_up = fbx_connection_status_details['bytes_up']
if bytes_down < 1000000 and bytes_up < 1000000:
    units = 'Ko'
    factor = 1000
elif bytes_down < 1000000000 and bytes_up < 1000000000:
    units = 'Mo'
    factor = 1000000
else :
    units = 'Go'
    factor = 1000000000
bytes_down /= factor
bytes_up /= factor
print('  Totaux entrant/sortant         {0:.1f}/{1:.1f} {2}'.format(bytes_down,bytes_up,units))
print('')

print('Informations secondaires :')
print('==========================')
print('')
info = 'Non'
if fbx_config['model_info']['has_vm']: info = 'Oui'
print('  Compatible VM(s)                    {0}'.format(info))
print('  Nombre d\'emplacements disques       {0}'.format(fbx_config['model_info']['customer_hdd_slots']))
info = 'Non'
if fbx_config['model_info']['has_home_automation']: info = 'Oui'
print('  Compatible domotique                {0}'.format(info))
info = 'Non'
if fbx_config['model_info']['has_lan_sfp']: info = 'Oui'
print('  Compatible LAN SFP                  {0}'.format(info))
info = 'Non'
if fbx_config['model_info']['has_dect']: info = 'Oui'
print('  Compatible DECT                     {0}'.format(info))
info = 'Non'
if fbx_config['model_info']['has_expansions']: info = 'Oui'
print('  Module(s) présent(s)                {0}'.format(info))
for expansion in fbx_config['expansions']:
    if expansion['present']:
        print('  Module {0:29}{1}'.format(str(expansion['slot']), expansion['type'].upper().replace('_',' ')))
print('')

print('Informations capteurs    :')
print('==========================')
print('')
for sensor in fbx_config['sensors']:
    if 'value' in sensor: temp = sensor['value']
    else: temp = '-'
    print('  {0:30}{1}°C'.format(sensor['name'], temp))
for fan in fbx_config['fans']:
    print('  {0:30}{1} tr/min'.format(fan['name'], fan['value']))
print('')

print('Téléphone :')
print('===========')
print('')
if fbx_phone[0]['on_hook'] == True:
    phone_status = 'Raccroché'
else:
    phone_status = 'Décroché'
print('  Etat du combiné                {0}'.format(phone_status))
if fbx_phone[0]['is_ringing'] == True:
    ring_status = 'Active'
else:
    ring_status = 'Inactive'
print('  Sonnerie                       {0}'.format(ring_status))
print('')

print('')
print('Services :')
print('==========')
print('')
status = fbx_media['enabled']
if status == 'active':
    status_str = 'Activé'
else :
    status_str = 'Désactivé'
print('  AirMedia                       {0}'.format(status_str))
fbx_data = fbx.ftp.get_ftp_configuration()
info = 'Désactivé'
if fbx_data['enabled']: info = 'Activé'
print('  {0:31}{1}'.format('FTP', info))
fbx_data = fbx.upnpav.get_configuration()
info = 'Désactivé'
if fbx_data['enabled']: info = 'Activé'
print('  {0:31}{1}'.format('UPnP AV', info))
fbx_data = fbx.upnpigd.get_configuration()
info = 'Désactivé'
if fbx_data['enabled']: info = 'Activé'
print('  {0:31}{1}'.format('UPnP IGD', info))
for srv in [ {'name': 'DynDNS', 'real': 'dyndns'}, {'name': 'OVH', 'real': 'ovh'}, {'name': 'No-IP', 'real': 'noip'} ]:
    fbx_data = fbx.connection.get_dyndns_config(srv['real'])
    info = 'Désactivé'
    if fbx_data['enabled']: info = 'Activé'
    print('  {0:31}{1}'.format('DNS dynamique ' + srv['name'], info))
fbx_data = fbx.netshare.get_afp_configuration()
info = 'Désactivé'
if fbx_data['enabled']: info = 'Activé'
print('  {0:31}{1}'.format('Partage AFP', info))
fbx_data = fbx.netshare.get_samba_configuration()
info = 'Désactivé'
if fbx_data['file_share_enabled']: info = 'Activé'
print('  {0:31}{1}'.format('Partage SAMBA/CiFS', info))
print('')

print('FTTH :')
print('======')
print('                         Descendant         Montant')
print('                         --                 --')
print('  Débit ATM              {0:6.1f} Mb/s       {1:6.1f} Mb/s'.format(fbx_connection_status_details['bandwidth_down']/1000000,fbx_connection_status_details['bandwidth_up']/1000000))
print('')
print(' Journal de connexion')
print(' --------------------')
print('')
print('  Date                      Type      Nom           Etat        Débit (Mb/s)')
print('  --                        --        --            --          --')
index = 0
while index < len(fbx_connection_logs):
    dat = time.strftime("%c", time.localtime(fbx_connection_logs[index]['date']))
    typ = fbx_connection_logs[index]['type']
    if typ == 'link':
        typ_str = 'Lien'
    elif typ == 'conn':
        typ_str = 'Connexion'
    else :
        typ_str = typ
    name = fbx_connection_logs[index][typ].upper()
    state = fbx_connection_logs[index]['state']
    underscore = name.find('_')
    if underscore != -1:
      name = name.replace('_',' (',1)
      name = name.replace('PUB','public')
      name += ')'
    if state == 'up':
        status = 'Connexion'
    else :
        status = 'Deconnexion'
    if typ == 'link':
        down = fbx_connection_logs[index]['bw_down']/1000000
        up = fbx_connection_logs[index]['bw_up']/1000000
        print('  {0}  {1:10.10s}{2:14.14s}{3:11.11s} {4:.0f}/{5:.0f}'.format(dat,typ_str,name,status,down,up))
    else :
        print('  {0}  {1:10.10s}{2:14.14s}{3:11.11s}'.format(dat,typ_str,name,status))
    index+=1
print('')

print('')
print('Wifi :')
print('======')
print('')
if fbx_wifi['enabled'] == True :
  status = 'Ok'
else :
  status = 'Off'
print('  Etat                           {0}'.format(status))
print('  SSID                           {0}'.format(fbx_bss[0]['config']['ssid']))
key = fbx_bss[0]['config']['encryption'].upper()
key = key.replace('_',' [',1)
key = key.replace('_','-')
key += ']'
print('  Type de clé                    {0}'.format(key))
info = 'Non'
if fbx_bss[0]['config']['hide_ssid']: info = 'Oui'
print('  SSID masqué                    {0}'.format(info))
info = 'Non autorisé'
if fbx_bss[0]['config']['wps_enabled']: info = 'Autorisé'
print('  WPS                            {0}'.format(info))
info = 'Non'
if fbx_bss[0]['use_shared_params']: info = 'Oui'
print('  Paramètres communs             {0}'.format(info))

print('')
print(' Interfaces')
print(' ----------')
print('')
print('  Carte  Largeur de bande  Etat     Canal primaire  Canal secondaire')
print('  --     --                --       --              --')
for ap in fbx_wifi_ap:
    info = 'Inactif'
    if ap['status']['state'] == 'active': info = 'Actif'
    auto = ''
    if ap['config']['primary_channel'] == 0 and ap['config']['secondary_channel'] == 0: auto = '[auto]'
    print('  {0:7}{1:18}{2:9}{3:16}{4}'.format(ap['name'], str(ap['status']['channel_width']) + ' Mhz', info, auto + str(ap['status']['primary_channel']), auto + str(ap['status']['secondary_channel'])))
print('')

print('')
print('Réseau :')
print('========')
print('')
print('  Adresse MAC Freebox            {0}'.format(fbx_config['mac']))
print('  Adresse IP                     {0}'.format(fbx_connection_status_details['ipv4']))
ipv6_status = fbx_ipv6['ipv6_enabled']
if ipv6_status == True:
    status = 'Activé'
else :
    status = 'Désactivé'
print('  IPv6                           {0}'.format(status))
print('  Adresse IPV6                   {0}'.format(fbx_connection_status_details['ipv6']))
if lan_config['mode'] == 'router':
    status = 'Activé'
else :
    status = 'Désactivé'
print('  Mode routeur                   {0}'.format(status))
print('  Adresse IP privée              {0}'.format(lan_config['ip']))
ip_dmz = dmz_config['ip']
if ip_dmz == '':
  ip_dmz = 'Désactivé'    
print('  Adresse IP DMZ                 {0}'.format(ip_dmz))
if fbx_connection_config['ping'] == True:
  status = 'Activé'
else :
  status = 'Désactivé'
print('  Réponse au ping                {0}'.format(status))
if fbx_connection_config['wol'] == True:
  status = 'Activé'
else :
  status = 'Désactivé'
print('  Proxy Wake On Lan              {0}'.format(status))
if fbx_dhcp_config['enabled'] == True:
  status = 'Activé'
else :
  status = 'Désactivé'
print('  Serveur DHCP                   {0}'.format(status))
print('  Plage d\'adresses dynamique     {0} - {1}'.format(fbx_dhcp_config['ip_range_start'],fbx_dhcp_config['ip_range_end']))
print('  Netmask                        {0}'.format(fbx_dhcp_config['netmask']))
print('  Filtrage NAC                   {0}'.format(fbx_wifi['mac_filter_state']))
#dns_list = ' '.join(fbx_dhcp_config['dns']).split()
dns_list = [x for x in fbx_dhcp_config['dns'] if x != '']
print('  DNS                            {0}'.format(*dns_list))
print('')
print(' Informations sur le SFP FTTH')
print(' ----------------------------')
print('') 
print('  Fabricant                      {0}'.format(fbx_connection_status_details['ftth']['sfp_vendor']))
print('  Modèle                         {0}'.format(fbx_connection_status_details['ftth']['sfp_model']))
print('  Type                           {0}'.format(fbx_connection_status_details['ftth']['link_type'].upper()))
print('  N° de série                    {0}'.format(fbx_connection_status_details['ftth']['sfp_serial']))
print('') 
index = 0
while index < len(fbx_static_dhcp):
    if index == 0:
        print('')
        print(' Attributions dhcp statiques :')
        print(' -----------------------------')
        print('') 
        print('  Hostname               Adresse MAC            Adresse IP')
        print('  --                     --                     --')
    mac = fbx_static_dhcp[index]['mac']
    hostname = fbx_static_dhcp[index]['hostname']
    ip = fbx_static_dhcp[index]['ip']
    print('  {0:21.21s}  {1:21.21s}  {2:21.21s}'.format(hostname,mac,ip))
    index += 1
index = 0
while index < len(fbx_dyn_dhcp):
    if fbx_dyn_dhcp[index]['is_static'] == False :
        if index == 0 :
            print('')
            print(' Attributions dhcp dynamiques :')
            print(' ----------------------------')
            print('') 
            print('  Hostname               Adresse MAC            Adresse IP')
            print('  --                     --                     --')
        mac = fbx_dyn_dhcp[index]['mac']
        hostname = fbx_dyn_dhcp[index]['hostname']
        ip = fbx_dyn_dhcp[index]['ip']
        print('  {0:21.21s}  {1:21.21s}  {2:21.21s}'.format(hostname,mac,ip))
    index += 1
print('')
print(' Redirections de ports sortants :')
print(' --------------------------------')
print('')
print('  Protocole  IP source         Port source  Destination       Nom               Port destination')
print('  --         --                --           --                --                --')
if fbx_ports != None:
    index = 0
    while index < len(fbx_ports):
        if fbx_ports[index]['enabled'] == True:
            ip_proto = fbx_ports[index]['ip_proto']
            wan_port_start = fbx_ports[index]['wan_port_start']
            wan_port_end = fbx_ports[index]['wan_port_end']
            lan_ip = fbx_ports[index]['lan_ip']
            src_ip = fbx_ports[index]['src_ip']
            if src_ip == '0.0.0.0':
                src_ip = 'Tout'
            lan_port = fbx_ports[index]['lan_port']
            hostname = fbx_ports[index]['hostname']
            print('  {0:9.9s}  {1:16.16s}  {2:<5d} {3:<5d}  {4:16.16s}  {5:16.16s}  {6}'.format(ip_proto.upper(),src_ip,wan_port_start,wan_port_end,lan_ip,hostname,lan_port))
        index += 1
print('')
print('')
print(' Redirections de ports entants :')
print(' -------------------------------')
print('')
print('  Type     Usage             Port   Actif  Autorisé')
print('  --       --                --     --     --')
fbx_data = fbx.fw.get_incoming_ports_configuration()
if fbx_data != None:
    index = 0
    while index < len(fbx_data):
        actif = 'Non'
        if fbx_data[index]['active']: actif = 'Oui'
        autorise = 'Non'
        if fbx_data[index]['active']: actif = 'Non'
        print('  {0:9}{1:16}{2:7d}  {3:7}{4}'.format(fbx_data[index]['type'].upper().replace('_','+'), fbx_data[index]['id'].upper().replace('_',' '), fbx_data[index]['in_port'], actif, autorise))
        index += 1
print('')
print(' Interfaces réseau :')
print(' -------------------')
print('')
print('  Freeplug           ID                 Lien  Role     Débit entrant            Débit sortant')
print('  --                 --                 --    --       --                       --')
if fbx_freeplugs != None:
    fp_idx = 0
    while fp_idx < len(fbx_freeplugs):
        mainid = fbx_freeplugs[fp_idx]['id']
        index = 0
        if 'members' in fbx_freeplugs[fp_idx]:
            while index < len(fbx_freeplugs[fp_idx]['members']):
                fpid = fbx_freeplugs[fp_idx]['members'][index]['id']
                status = fbx_freeplugs[fp_idx]['members'][index]['has_network']
                if status == True:
                    stat = "Ok"
                else:
                    stat = "Off"
                role = fbx_freeplugs[fp_idx]['members'][index]['net_role']
                if role == 'cco':
                    role = 'Coord. '
                elif role == 'pco':
                    role = 'PCoord.'
                else:
                    role = 'Station'
                if status == True:
                    rx = fbx_freeplugs[fp_idx]['members'][index]['rx_rate']
                    tx = fbx_freeplugs[fp_idx]['members'][index]['tx_rate']
                    if rx == -1:
                        rx = 0
                    if tx == -1:
                        tx = 0
                    rx_str = '{0:.0f} Mb/s'.format(rx)
                    tx_str = '{0:.0f} Mb/s'.format(tx)
                    print('  {0:17.17s}  {1:17.17s}  {2:4.4s}  {3:7.7s}  {4:23.23s}  {5:23.23s}'.format(mainid, fpid, stat, role, rx_str.ljust(23," "), tx_str.ljust(23," ")))
                else :
                    print('  {0:17.17s}  {1:17.17s}  Non connecté'.format(mainid,fpid))
                index += 1
        fp_idx += 1
print('')
print('                         Lien           Débit entrant            Débit sortant')
print('                         --             --                       --')
# Updates all bandwidths
stats = [None] * len(fbx_switch_status)
index = 0
while index < len(fbx_switch_status):
    stats[index] = fbx.switch.get_port_stats(fbx_switch_status[index]['id'])
    index += 1
fbx_connection_status_details = fbx.connection.get_status_details()
rx = fbx_connection_status_details['rate_down']/1024
rxb = rx*8/1024
tx = fbx_connection_status_details['rate_up']/1024
txb = tx*8/1024
rx_str = '{0:.0f} ko/s ({1:.1f} Mb/s)'.format(rx, rxb)
tx_str = '{0:.0f} ko/s ({1:.1f} Mb/s)'.format(tx, txb)
print('  {0:21.21s}  {1:13.13s}  {2}  {3}'.format('WAN', '', rx_str.ljust(23," "), tx_str.ljust(23," ")))
index = 0
fp_idx = 0
mac_fp_list = []
if fbx_freeplugs != None:
    while fp_idx < len(fbx_freeplugs):
        if 'members' in fbx_freeplugs[fp_idx]:
            maclist = fbx_freeplugs[fp_idx]['members'][:][:]
            mac_fp_list = [ (d['id']) for d in maclist]
        fp_idx += 1
while index < len(fbx_switch_status):
    name = fbx_switch_status[index]['name']
    link = fbx_switch_status[index]['mode']
    if fbx_switch_status[index]['link'] == 'up':
        rx = stats[index]['rx_bytes_rate']/1024
        tx = stats[index]['tx_bytes_rate']/1024
        rx_str = '{0:.0f} ko/s'.format(rx)
        tx_str = '{0:.0f} ko/s'.format(tx)
        print('  {0:21.21s}  {1:13.13s}  {2}  {3}'.format(name, link, rx_str.ljust(23," "), tx_str.ljust(23," ")))
        if 'mac_list' in fbx_switch_status[index]:
            for x in fbx_switch_status[index]['mac_list']:
                if x['mac'] not in mac_fp_list:
                    print('    {0}'.format(x['hostname']))
    else :
        print('  {0:21.21s}  Non connecté'.format(name))
    index += 1
print('')
print(' Filtrage NAC :')
print(' --------------')
print('')
print('  {0:25}  {1:25}  {2:17}  {3}'.format('Nom','Hôte','Adresse Mac','Filtre'))
print('  {0:25}  {1:25}  {2:17}  {3}'.format('--','--','--','--'))
print('')
for nac in fbx.wifi.get_wifi_mac_filters():
    print('  {0:25}  {1:25}  {2:17}  {3}'.format(nac['host']['primary_name'], nac['hostname'], nac['mac'], nac['type']))
print('')

print('')
print('Clients connus :')
print('================')
print('')
print('  {0:25}  {1:17}  {2:10}  {3:12}  {4}'.format('Nom','Adresse MAC','Interface','Etat','Constructeur'))
print('  {0:25}  {1:17}  {2:10}  {3:12}  {4}'.format('--','--','--','--','--'))
print('')
fbx_data = fbx.lan.get_interfaces()
for interf in fbx_data:
    for clt in fbx.lan.get_hosts_list(interf['name']):
        info = 'Non connecté'
        if clt['active']: info = 'Connecté'
        print('  {0:25}  {1:17}  {2:10}  {3:12}  {4}'.format(clt['primary_name'], clt['l2ident']['id'], interf['name'], info, clt['vendor_name']))
print('')

print('')
print('Profils de restrictions :')
print('=========================')
print('')
print('  {0:20}  {1:25}  {2:8}  {3}'.format('Nom','Client','Etat','Interdiction'))
print('  {0:20}  {1:25}  {2:8}  {3}'.format('--','--','--','--'))
print('')
for prf in fbx.profile.get_netcontrols():
    name = prf['profile_name']
    state = 'Autorisé'
    if prf['current_mode'] == 'denied': state = 'Interdit'
    ranges = ''
    for rul in fbx.profile.get_netcontrol_rules(prf['profile_id']):
        if rul['enabled']:
            start = rul['start_time']
            stop = rul['end_time']
            start /= 300
            stop /= 300
            startH = start / 12
            stopH = stop / 12
            startM = start - (12 * startH)
            stopM = stop - (12 * stopH)
            if ranges == '': ranges = f"{startH:.0f}h{startM:.0f}-{stopH:.0f}h{stopM:.0f}"
            else: ranges = ranges + f", {startH:.0f}h{startM:.0f}-{stopH:.0f}h{stopM:.0f}"
    for clt in prf['hosts']: print('  {0:20}  {1:25}  {2:8}  {3}'.format(name, clt['primary_name'], state, ranges))
print('')

print('')
print('Serveurs VPN :')
print('==============')
print('')
print('  {0:15}  {1:31}  {2:5}  {3:4}  {4:4}  {5:7}  {6}'.format('Nom','VLAN','PAT','IPv4', 'IPv6','Etat','Utilisateurs'))
print('  {0:15}  {1:31}  {2:5}  {3:4}  {4:4}  {5:7}  {6}'.format('--','--','--','--','--','--','--'))
for vpn in fbx.vpn.get_server_list():
    if vpn['state'] == 'started':
        fbx_data = fbx.vpn.get_server_config(vpn['name'])
        ip4 = 'Non'
        if fbx_data['enable_ipv4']: ip4 = 'Oui'
        ip6 = 'Non'
        if fbx_data['enable_ipv6']: ip6 = 'Oui'
        users = ''
        for usr in fbx.vpn.get_server_users():
            if users == '': users = usr['login']
            else: users = users + ', ' + usr['login']
        print('  {0:15}  {1:31}  {2:5}  {3:4}  {4:4}  {5:7}  {6}'.format(vpn['name'].upper().replace('_',' '), fbx_data['ip_start'] + '-' + fbx_data['ip_end'], fbx_data['port_nat'], ip4, ip6, 'Actif', users))
    else: print('  {0:15}  {1:31}  {2:5}  {3:4}  {4:4}  {5:7}'.format(vpn['name'].upper().replace('_',' '),'-','-','-','-','Inactif'))
print('')

print('')
print('Clients VPN :')
print('=============')
print('')
print('  {0:25}  {1:7}  {2:12}  {3:10}  {4:25}  {5:15}  {6:15}  {7}'.format('Nom','Type','Utilisateur','Etat', 'Hôte','IP', 'DNS', 'Passerelle'))
print('  {0:25}  {1:7}  {2:12}  {3:10}  {4:25}  {5:15}  {6:15}  {7}'.format('--','--','--','--','--','--','--','--'))
for vpn in fbx.vpn.get_client_list():
    typ = vpn['type'].upper()
    name = vpn['description']
    host = '-'
    ip = '-'
    dns = '-'
    mask = '-'
    gtw = '-'
    state = 'Inactif'
    if typ == 'PPTP':
        user = vpn['conf_pptp']['username']
        host = vpn['conf_pptp']['remote_host']
    else: user = vpn['conf_openvpn']['username']
    if vpn['active']:
        state = 'Déconnecté'
        fbx_data = fbx.vpn.get_client_status()
        if fbx_data['state'] == 'up': state = 'Connecté'
        ip = fbx_data['ipv4']['ip_mask']['ip']
        mask = fbx_data['ipv4']['ip_mask']['mask']
        dns = fbx_data['ipv4']['dns'][0]
        gtw = fbx_data['ipv4']['gateway']
    print('  {0:25}  {1:7}  {2:12}  {3:10}  {4:25}  {5:15}  {6:15}  {7}'.format(name, typ, user, state, host, ip, dns, gtw))
print('')

print('')
print('Stockage :')
print('==========')
print('')
print(' Partitions RAID :')
print(' -----------------')
print('')
print('  {0:12}  {1:4}  {2:7}  {3:5}  {4:8}  {5:12}  {6}'.format('Nom','Type','Dégradé','Monté','Taille','Utilisation','Disponible'))
print('  {0:12}  {1:4}  {2:7}  {3:5}  {4:8}  {5:12}  {6}'.format('--','--','--','--','--','--','--'))
print('')
for raid in fbx.storage.get_raids():
    state = 'Non'
    if raid['degraded']: state = 'Oui'
    mounted = 'Non'
    fbx_data = fbx.storage.get_partition(raid['disk_id'])
    if fbx_data['state'] == 'mounted': mounted = 'Oui'
    size = '{0:.0f}'.format(raid['array_size'] / 1000000000) + ' GB'
    free = '{0:.2f}'.format(fbx_data['free_bytes']  / 1000000000) + ' GB'
    used = '{0:.2f}'.format(fbx_data['used_bytes']  / 1000000000) + ' GB'
    print('  {0:12}  {1:4}  {2:7}  {3:5}  {4:8}  {5:12}  {6}'.format(raid['name'], raid['level'].replace('raid',''), state, mounted, size, used, free))
print('')
print(' Membres RAID :')
print(' -----------------')
print('')
print('  {0:12}  {1:25}  {2:20}  {3:4}  {4:8}  {5}'.format('RAID','Modèle','N° de série','Slot','Taille','Température'))
print('  {0:12}  {1:25}  {2:20}  {3:4}  {4:8}  {5}'.format('--','--','--','--','--','--'))
print('')
raiddisk = []
for raid in fbx.storage.get_raids():
    raiddisk.append(raid['disk_id'])
    for member in raid['members']:
        raiddisk.append(member['id'])
        size = '{0:.0f}'.format(member['total_bytes'] / 1000000000) + ' GB'
        print('  {0:12}  {1:25}  {2:20}  {3:4}  {4:8}  {5}'.format(member['set_name'], member['disk']['model'], member['disk']['serial'], member['device_location'].replace('sata-internal-p',''), size, str(member['disk']['temp']) + '°C'))
print('')
print(' Disques supplémentaires :')
print(' -------------------------')
print('')
print('  {0:12}  {1:25}  {2:20}  {3:10}  {4:5}  {5:8}  {6:12}  {7:12} {8}'.format('Nom','Modèle','N° de série','Type','Monté','Taille','Utilisation','Disponible','Température'))
print('  {0:12}  {1:25}  {2:20}  {3:10}  {4:5}  {5:8}  {6:12}  {7:12} {8}'.format('--','--','--','--','--','--','--','--','--'))
print('')
for disk in fbx.storage.get_disks():
    if disk['id'] not in raiddisk:
        size = '{0:.0f}'.format(disk['total_bytes'] / 1000000000) + ' GB'
        temp = str(disk['temp'])
        if temp == '0': temp = '-'
        else: temp = temp + '°C'
        model = disk['model']
        if model == '': model = '-'
        serial = disk['serial']
        if serial == '': serial = '-'
        typ = disk['type'].upper() + '/' + disk['partitions'][0]['fstype'].upper()
        name = disk['partitions'][0]['label']
        mounted = 'Non'
        if disk['partitions'][0]['state'] == 'mounted': mounted = 'Oui'
        free = '{0:.2f}'.format(disk['partitions'][0]['free_bytes']  / 1000000000) + ' GB'
        used = '{0:.2f}'.format(disk['partitions'][0]['used_bytes']  / 1000000000) + ' GB'        
        print('  {0:12}  {1:25}  {2:20}  {3:10}  {4:5}  {5:8}  {6:12}  {7:12} {8}'.format(name, model, serial, typ, mounted, size, used, free, temp))
print('')

print('')
print('Freebox OS :')
print('============')
print('')
info = 'Désactivé'
if fbx_connection_config['remote_access']: info = str(fbx_connection_config['remote_access_port'])
print('  Port d\'accès distant   {0}'.format(info))
info = 'Désactivé'
if fbx_connection_config['https_available']: info = str(fbx_connection_config['https_port'])
print('  Port HTTPS             {0}'.format(info))
info = 'Activé'
if fbx_connection_config['disable_guest']: info = 'Désactivé'
print('  Accès invité           {0}'.format(info))
info = 'Désactivé'
if fbx_connection_config['adblock'] and not fbx_connection_config['adblock_not_set']: info = 'Activé'
print('  Bloqueur de pubs       {0}'.format(info))
info = 'Non autorisé'
if fbx_connection_config['allow_token_request']: info = 'Autorisé'
print('  Token de connexion     {0}'.format(info))
info = 'Sans'
if fbx_connection_config['is_secure_pass']: info = 'Avec'
print('  Pass sécurité          {0}'.format(info))
info = 'Désactivé'
if fbx_connection_config['api_remote_access']:
    info = 'Activé'
    print('  Accès distant à l\'API  {0}'.format(info))
    print('  DNS de l\'API           {0}'.format(fbx_connection_config['api_domain']))
else: print('  Accès distant à l\'API  {0}'.format(info))
print('')

print('')
print('VM :')
print('====')
print('')
print('  {0:12}  {1:4}  {2:5}  {3:3}  {4:5}  {5:10}  {6:8}  {7}'.format('Nom','VCPU','RAM','USB','Ecran','OS','Etat','MAC'))
print('  {0:12}  {1:4}  {2:5}  {3:3}  {4:5}  {5:10}  {6:8}  {7}'.format('--','--','--','--','--','--','--','--'))
print('')
for vm in fbx.vm.get_config_all():
    name = vm['name']
    vcpu = vm['vcpus']
    ram = '{0:.0f}'.format(vm['memory'] / 1024) + ' GB'
    usb = 'Oui'
    if vm['bind_usb_ports'] == None: usb = 'Non'
    screen = 'Non'
    if vm['enable_screen']: screen = 'Oui'
    os = vm['os']
    state = 'Arrêtée'
    if vm['status'] == 'running': state = 'Démarrée'
    mac = vm['mac'].upper()
    print('  {0:12}  {1:4}  {2:5}  {3:3}  {4:5}  {5:10}  {6:8}  {7}'.format(name, vcpu, ram, usb, screen, os, state, mac))
print('')

print('')
print('Téléchargements :')
print('=================')
print('')
fbx_data = fbx.downloads.get_config()
print('  Tâches simultanées       {0}'.format(fbx_data['max_downloading_tasks']))
if fbx_data['use_watch_dir']: print('  Répertoire surveillé     {0}'.format(base64.b64decode(fbx_data['download_dir'].encode('utf-8')).decode('utf-8')))
else: print('  Répertoire surveillé     {0}'.format('Aucun'))
print('  Serveurs DNS             {0}, {1}'.format(fbx_data['dns1'], fbx_data['dns2']))
if fbx_data['bt'] == None: print('  BitTorrent               {0}'.format('Désactivé'))
else:
    print('  BitTorrent               {0}'.format('Activé'))
    print('  Pairs maximum            {0}'.format(fbx_data['bt']['max_peers']))
    print('  Temps d\'annonce max      {0}s'.format(fbx_data['bt']['announce_timeout']))
    print('  Ratio par défaut         {0}'.format(fbx_data['bt']['stop_ratio']))
    if fbx_data['throttling']['mode'] == 'normal':
        up = '{0:.0f}'.format(fbx_data['throttling']['normal']['rx_rate'] / 1048576)
        if up == '0': up = 'Illimité'
        else: up = up + ' MBps'
        dwn = '{0:.0f}'.format(fbx_data['throttling']['normal']['tx_rate'] / 1048576)
        if dwn == '0': dwn = 'Illimité'
        else: dwn = dwn + ' MBps'
        print('  Débit montant            {0}'.format(up))
        print('  Débit descendant         {0}'.format(dwn))
    elif fbx_data['throttling']['mode'] == 'slow':
        up = '{0:.0f}'.format(fbx_data['throttling']['slow']['rx_rate'] / 1048576)
        if up == '0': up = 'Illimité'
        else: up = up + ' MBps'
        dwn = '{0:.0f}'.format(fbx_data['throttling']['slow']['tx_rate'] / 1048576)
        if dwn == '0': dwn = 'Illimité'
        else: dwn = dwn + ' MBps'
        print('  Débit montant            {0}'.format(up))
        print('  Débit descendant         {0}'.format(dwn))
    elif fbx_data['throttling']['mode'] == 'schedule':
        up = '{0:.0f}'.format(fbx_data['throttling']['normal']['rx_rate'] / 1048576)
        if up == '0': up = 'Illimité'
        else: up = up + ' MBps'
        dwn = '{0:.0f}'.format(fbx_data['throttling']['normal']['tx_rate'] / 1048576)
        if dwn == '0': dwn = 'Illimité'
        else: dwn = dwn + ' MBps'
        print('  Débit montant            {0}'.format(up))
        print('  Débit descendant         {0}'.format(dwn))
        up = '{0:.0f}'.format(fbx_data['throttling']['slow']['rx_rate'] / 1048576)
        if up == '0': up = 'Illimité'
        else: up = up + ' MBps'
        dwn = '{0:.0f}'.format(fbx_data['throttling']['slow']['tx_rate'] / 1048576)
        if dwn == '0': dwn = 'Illimité'
        else: dwn = dwn + ' MBps'
        print('  Débit montant réduit     {0}'.format(up))
        print('  Débit descendant réduit  {0}'.format(dwn))
    else:  print('  Aucun débit autorisé     {0}'.format(dwn))
if fbx_data['news'] == None: print('  News                     {0}'.format('Désactivées'))
else:
    print('  News                     {0}'.format('Activées'))
    print('  Serveur                  {0}'.format(fbx_data['news']['server']))
    print('  Utilisateur              {0}'.format(fbx_data['news']['user']))
    print('  Fils parallèles          {0}'.format(fbx_data['news']['nthreads']))
    info = 'Non'
    if fbx_data['news']['ssl']: info = 'Oui'
    print('  SSL                      {0}'.format(info))
    info = 'Non'
    if fbx_data['news']['auto_extract']: info = 'Oui'
    print('  Auto-extraction          {0}'.format(info))
    info = 'Non'
    if fbx_data['news']['auto_repair']: info = 'Oui'
    print('  Auto-réparation          {0}'.format(info))
print('')
print(' Tâches :')
print(' --------')
print('')
print('  {0:60}  {1:12}  {2:8}  {3:11}'.format('Téléchargement','Etat','Taille','Ratio'))
print('  {0:60}  {1:12}  {2:8}  {3:11}'.format('--','--','--','--'))
print('')
states = {'stopped': 'Arrêté', 'queued': 'En attente', 'starting': 'Préparation', 'downloading': 'Téléchargement',
          'stopping': 'Arrêt', 'error': 'En erreur', 'done': 'Terminé', 'checking': 'Vérification',
          'repairing': 'Réparation', 'extracting': 'Extraction', 'seeding': 'Partage', 'retry': 'Relance'}
for dwnl in fbx.downloads.get_tasks():
    size = '{0:.3f} GB'.format(dwnl['size'] / 1073741824)
    ratio = '{0:.4f}/{1:.2f}'.format(dwnl['tx_bytes'] / dwnl['size'],dwnl['stop_ratio'] / 100)
    print('  {0:60.60}  {1:12}  {2:8}  {3:11}'.format(dwnl['name'],states[dwnl['status']],size,ratio))

# Close freebox session
fbx.close()
