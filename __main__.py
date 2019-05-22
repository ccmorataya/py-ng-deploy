import os
# import subprocess as sp
import sys
import json

from .bld import ng_py_build
from .upload import ng_py_upload

def main():
    if len(sys.argv) == 1:
        # TODO-CM: add ascii art
        print('ng-py-deploy\n')
        print('Usage:')
        print('  ng-py-deploy (prod | dev) [hash]')
        sys.exit()

    if len(sys.argv) > 1:
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

if __name__ == '__main__':
    main()
