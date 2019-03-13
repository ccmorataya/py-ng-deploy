import pysftp
import os

cnopts = pysftp.CnOpts()
cnopts.hostkeys = None

host = ''
username = ''
password = ''
srv = pysftp.Connection(host=host, username=username, password=password, cnopts=cnopts)

remote_dir = ''
local_dir = ''

print('Backup to '+ os.path.abspath(local_dir) + '')    # '' = backup_folder
srv.chdir(remote_dir)
srv.get_r('.', local_dir + '', preserve_mtime=True)     # '' = backup_folder
print('Done :D')
print('Uploading to ' + remote_dir)
srv.put_r(local_dir + '', remote_dir, preserve_mtime=True)  # '' = angular_compiled_folder_inside_dist
print('Done :D')

srv.close()
