import pysftp
import os
import json

cnopts = pysftp.CnOpts()
cnopts.hostkeys = None

with open('config.json') as json_config:
    data = json.load(json_config)

srv = pysftp.Connection(host=data['host'], username=data['username'], password=data['password'], cnopts=cnopts)

print('Backup to '+ os.path.abspath(data['local_dir']) + data['backup_folder'])
srv.chdir(data['remote_dir'])
# TODO-CM: validate if the backup_folder exists
srv.get_r('.', data['local_dir'] + data['backup_folder'], preserve_mtime=True)
print('Done :D')
print('Uploading to ' + data['remote_dir'])
srv.put_r(data['local_dir'] + data['base'], data['remote_dir'], preserve_mtime=True)
print('Done :D')

srv.close()
