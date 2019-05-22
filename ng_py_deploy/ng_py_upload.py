import pysftp
import os
import json

json_data = {}
with open('.ngpydeployrc') as json_config:
    json_data = json.load(json_config)

def upload():
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None

    srv = pysftp.Connection(host=json_data['host'], username=json_data['username'], password=json_data['password'], cnopts=cnopts)
    backup_path = json_data['angular_project_root'] + json_data['local_dir'] + json_data['backup_folder']
    base_path = json_data['angular_project_root'] + json_data['local_dir'] + json_data['base']

    print('Backup to '+ backup_path)
    srv.chdir(json_data['remote_dir'])
    if not os.path.isdir(backup_path):
        print('Backup path doesn\'t exists, creating')
        os.mkdir(backup_path)
    srv.get_r('.', backup_path, preserve_mtime=True)
    print('Done :D')
    print('Uploading to ' + json_data['remote_dir'])
    srv.put_r(base_path, json_data['remote_dir'], preserve_mtime=True)
    print('Done :D')

    srv.close()
