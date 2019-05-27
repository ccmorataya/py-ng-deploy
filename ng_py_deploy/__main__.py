import os
import sys
import json
import shutil

from pyfiglet import Figlet
from pathlib import Path
from ng_py_deploy import __version__
from ng_py_deploy import ng_py_build
from ng_py_deploy import ng_py_upload

NG_ROOT_DIR = os.getcwd()

def main():
    if len(sys.argv) == 1:
        f = Figlet(font='big')
        print(f.renderText('ngPyDeploy'))
        print(f'Version: {__version__}\n')
        print('Usage:')
        print('  ng_py_deploy (prod | dev) [hash]')
        sys.exit()
    elif len(sys.argv) > 1:
        do_init = initialize(sys.argv[1])

        if not do_init:
            result = ng_py_build.build(sys.argv[1])
            if result.returncode == 0:
                if len(sys.argv) > 2:
                    ng_py_build.gen_hash(sys.argv[2])

                ng_py_upload.upload()
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
        dest_rcfile = f'{NG_ROOT_DIR}/.ngpydeployrc'
        rc_file = Path(dest_rcfile)
        src_rcfile = f'{os.path.dirname(os.path.abspath(__file__))}/.ngpydeployrc'
        if not rc_file.is_file():
            shutil.copy(src_rcfile, dest_rcfile)
            print('Configuration file created')
            print('Please edit the file .ngpydeployrc with the given keys')
        else:
            print('.ngpydeployrc file already exists')
            print('Verify it and their config keys')
        # CM: do init stuff
        # * IF not exist rc file THEN
        #     create file inside project root based on config.json AND
        #     warn to user to edit the keys

        return True
    else:
        return False

if __name__ == '__main__':
    main()
