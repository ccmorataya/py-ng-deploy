import pysftp
import os
import json

cnopts = pysftp.CnOpts()
cnopts.hostkeys = None

with open('config.json') as json_config:
    json_data = json.load(json_config)

srv = pysftp.Connection(host=json_data['host'], username=json_data['username'], password=json_data['password'], cnopts=cnopts)

print('Backup to '+ os.path.abspath(json_data['angular_project_root'] + json_data['local_dir']) + json_data['backup_folder'])
srv.chdir(json_data['remote_dir'])
# TODO-CM: validate if the backup_folder exists if not create it
srv.get_r('.', json_data['angular_project_root'] + json_data['local_dir'] + json_data['backup_folder'], preserve_mtime=True)
print('Done :D')
print('Uploading to ' + json_data['remote_dir'])
srv.put_r(json_data['angular_project_root'] + json_data['local_dir'] + json_data['base'], json_data['remote_dir'], preserve_mtime=True)
print('Done :D')

srv.close()
