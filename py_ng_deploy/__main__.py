import os
import sys
import json
import shutil

from pathlib import Path
from py_ng_deploy import __version__
from py_ng_deploy import py_ng_build
from py_ng_deploy import py_ng_upload

RCFILE = '.pyngdeployrc'


def main():
    if len(sys.argv) == 1:
        print('                         _____             _')
        print('                        |  __ \\           | |')
        print(' _ __  _   _ _ __   __ _| |  | | ___ _ __ | | ___  _   _')
        print(
            '| \'_ \\| | | | \'_ \\ / _` | |  | |/ _ \\ \'_ \\| |/ _ \\| | | |'
              )
        print('| |_) | |_| | | | | (_| | |__| |  __/ |_) | | (_) | |_| |')
        print('| .__/ \\__, |_| |_|\\__, |_____/ \\___| .__/|_|\\___/ \\__, |')
        print('| |     __/ |       __/ |           | |             __/ |')
        print('|_|    |___/       |___/            |_|            |___/')
        print(f'Version: {__version__}\n')
        print('Usage:')
        print('  pyngDeploy (init | prod | dev) [--hash | --restore]')
        sys.exit()
    elif len(sys.argv) > 1:
        if not initialize(sys.argv[1]):
            if len(sys.argv) == 2 or (len(sys.argv) > 2 and not restoring(sys.argv[1], sys.argv[2], True)):
                result = py_ng_build.build(sys.argv[1])
                if result.returncode == 0 and len(sys.argv) > 2:
                    py_ng_build.gen_hash(sys.argv[2], json_find())
                py_ng_upload.upload(sys.argv[1], json_find(), False, os.name == 'posix')
            else:
                if restoring(sys.argv[1], sys.argv[2], False):
                    return
                else:
                    print('[pyngDeploy]:: Nothing to do')
                    sys.exit()
                    # spCallParams = []
                    # if os.name == 'nt':
                    #     spCallParams.append('bash.exe')
                    #     spCallParams.append('-c')
                    # spCallParams.append('python')
                    # spCallParams.append('upload.py')

                    # result = sp.call(spCallParams, stderr=sp.DEVNULL)
                    # if result == 0:
                    #     print('Process complete :D')
                    # else:
                    #     print('Something fails :O')


def initialize(init_keyword):
    if init_keyword == 'init':
        rc_file = Path(RCFILE)
        src_rcfile = f'{os.path.dirname(os.path.abspath(__file__))}/{RCFILE}'
        if not rc_file.is_file():
            shutil.copy(src_rcfile, RCFILE)
            print('Configuration file created')
            print(f'Please edit the file {RCFILE} with the given keys')
        else:
            print(f'{RCFILE} file already exists')
            print('Verify it and their config keys')
        return True
    else:
        return check_rcfile()


def check_rcfile():
    if Path(RCFILE).is_file():
        return False
    else:
        sys.exit(f'{RCFILE} not found, please init project')


def json_find():
    json_file = {}
    try:
        with open('angular.json') as json_config:
            json_file = json.load(json_config)
    except FileNotFoundError:
        sys.exit('angular.json file not found,'
                 ' verify that you are in an angular project folder')
    return iter_finder(json_file, 'outputPath')


def iter_finder(input_dict, key):
    if key in input_dict:
        return input_dict[key]
    for value in input_dict.values():
        if isinstance(value, dict):
            res = iter_finder(value, key)
            if res is not None:
                return res
    return None


def restoring(environment, restore_flag, validation):
    if environment != 'init' and restore_flag == '--restore':
        if not validation:
            print(f'RESTORING LAST BACKUP!')
            py_ng_upload.upload(environment, json_find(), True, os.name == 'posix')
        return True
    else:
        return False


if __name__ == '__main__':
    main()
