import pysftp
import os
import json
import sys

srv = None
json_data = {}
try:
    with open('.pyngdeployrc') as json_config:
        json_data = json.load(json_config)
except FileNotFoundError:
    pass


def host_key_check():
    cnopts = pysftp.CnOpts()
    hostkeys = None

    if cnopts.hostkeys.lookup(json_data['host']) is None:
        print('[pyngDeploy]:: New host - accepting any host key')
        hostkeys = cnopts.hostkeys
        cnopts.hostkeys = None
        with pysftp.Connection(host=json_data['host'],
                               username=json_data['username'],
                               password=json_data['password'],
                               cnopts=cnopts) as sftp:
            if hostkeys is not None:
                print(
                    '[pyngDeploy]:: Connected to new host, caching its hostkey'
                    )
                hostkeys.add(json_data['host'],
                             sftp.remote_server_key.get_name(),
                             sftp.remote_server_key)
                hostkeys.save(pysftp.helpers.known_hosts())

    return pysftp.Connection(host=json_data['host'],
                             username=json_data['username'],
                             password=json_data['password'],
                             cnopts=cnopts)


def upload(output_path, restore_deployment, is_posix):
    srv = host_key_check()
    backup_path = f'./dist/bkp' if is_posix else r'.\dist\bkp'
    base_path = f'./{output_path}' if is_posix else f'.\\{output_path}'

    if not restore_deployment:
        print('[pyngDeploy]:: Backup to ' + os.path.abspath(backup_path))
        srv.chdir(json_data['remote_dir'])
        if not os.path.isdir(backup_path):
            os.mkdir(backup_path)
        srv.get_r('.', backup_path, preserve_mtime=True)
        print('[pyngDeploy]:: Done :D')
        print('[pyngDeploy]:: Uploading to ' + json_data['remote_dir'])
        if is_posix:
            srv.put_r(base_path, json_data['remote_dir'], preserve_mtime=True)
        else:
            portable_put_r(base_path, json_data['remote_dir'])
    else:
        if not os.path.isdir(backup_path):
            sys.exit(f'There is no backup at {os.path.abspath(backup_path)}')
        else:
            print(f"""[pyngDeploy]:: Restoring backup from:
            {os.path.abspath(backup_path)}""")
            print(f'[pyngDeploy]:: To: {json_data["remote_dir"]}')
            if is_posix:
                srv.put_r(backup_path,
                          json_data['remote_dir'],
                          preserve_mtime=True)
            else:
                portable_put_r(backup_path, json_data['remote_dir'])
    print('[pyngDeploy]:: Done :D')
    srv.close()


def portable_put_r(ldir, rdir):
    for file in os.listdir(ldir):
        newFile = ldir + '\\' + file
        newR = rdir + '/' + file
        if (os.path.isdir(newFile)):
            srv.mkdir(newR)
            portable_put_r(newFile, newR)
        else:
            srv.put(newFile, newR)
