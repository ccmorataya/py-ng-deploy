import pysftp
import os
import sys
import configparser

from colorama import Fore

config = configparser.ConfigParser()
config.read('.pyngdeployrc')
srv = None


def host_key_check(environment):
    cnopts = pysftp.CnOpts()
    hostkeys = None

    if cnopts.hostkeys.lookup(config[environment]['Host']) is None:
        print(f'{Fore.CYAN}[pyngDeploy]:: New host - accepting any host key')
        hostkeys = cnopts.hostkeys
        cnopts.hostkeys = None
        with pysftp.Connection(host=config[environment]['Host'],
                               username=config[environment]['Username'],
                               password=config[environment]['Password'],
                               cnopts=cnopts) as sftp:
            if hostkeys is not None:
                print(
                    f'{Fore.CYAN}[pyngDeploy]:: Connected to new host, caching its hostkey'
                    )
                hostkeys.add(config[environment]['Host'],
                             sftp.remote_server_key.get_name(),
                             sftp.remote_server_key)
                hostkeys.save(pysftp.helpers.known_hosts())

    return pysftp.Connection(host=config[environment]['Host'],
                             username=config[environment]['Username'],
                             password=config[environment]['Password'],
                             cnopts=cnopts)


def upload(environment, output_path, restore_deployment, is_posix):
    srv = host_key_check(environment)
    backup_path = f'./dist/bkp' if is_posix else r'.\dist\bkp'
    base_path = f'./{output_path}' if is_posix else f'.\\{output_path}'

    if not restore_deployment:
        print(f'{Fore.CYAN}[pyngDeploy]:: Backup to ' + os.path.abspath(backup_path))
        srv.chdir(config[environment]['RemoteDir'])
        if not os.path.isdir(backup_path):
            os.mkdir(backup_path)
        srv.get_r('.', backup_path, preserve_mtime=True)
        print(f'{Fore.GREEN}[pyngDeploy]:: Done :D')
        print(f'{Fore.CYAN}[pyngDeploy]:: Uploading to ' + config[environment]['RemoteDir'])
        if is_posix:
            srv.put_r(base_path, config[environment]['RemoteDir'], preserve_mtime=True)
        else:
            portable_put_r(base_path, config[environment]['RemoteDir'])
    else:
        if not os.path.isdir(backup_path):
            sys.exit(f'{Fore.YELLOW}There is no backup at {os.path.abspath(backup_path)}')
        else:
            print(f'{Fore.CYAN}[pyngDeploy]:: Restoring backup from: '
                  f'{Fore.CYAN}{os.path.abspath(backup_path)}')
            print(f'{Fore.CYAN}[pyngDeploy]:: To: {config[environment]["RemoteDir"]}')
            if is_posix:
                srv.put_r(backup_path,
                          config[environment]['RemoteDir'],
                          preserve_mtime=True)
            else:
                portable_put_r(backup_path, config[environment]['RemoteDir'])
    print(f'{Fore.GREEN}[pyngDeploy]:: Done :D')
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
