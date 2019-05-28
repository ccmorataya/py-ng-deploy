import pysftp
import os
import json
import sys

json_data = {}
try:
    with open('.pyngdeployrc') as json_config:
        json_data = json.load(json_config)
except FileNotFoundError:
    pass

def upload(outputPath, restore_deployment):
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None

    srv = pysftp.Connection(host=json_data['host'], username=json_data['username'], password=json_data['password'], cnopts=cnopts)
    backup_path = f'./dist/bkp'
    base_path = f'./{outputPath}'

    if not restore_deployment:
        print('Backup to '+ os.path.abspath(backup_path))
        srv.chdir(json_data['remote_dir'])
        if not os.path.isdir(backup_path):
            os.mkdir(backup_path)
        srv.get_r('.', backup_path, preserve_mtime=True)
        print('Done :D')
        print('Uploading to ' + json_data['remote_dir'])
        srv.put_r(base_path, json_data['remote_dir'], preserve_mtime=True)
    else:
        if not os.path.isdir(backup_path):
            sys.exit(f'There is no backup at {os.path.abspath(backup_path)}')
        else:
            print(f'Restoring backup from: {os.path.abspath(backup_path)}')
            print(f'To: {json_data["remote_dir"]}')
            srv.put_r(backup_path, json_data['remote_dir'], preserve_mtime=True)
    print('Done :D')
    srv.close()
