import os
import subprocess as sp
import sys
import json

if len(sys.argv) == 1:
    # TODO-CM: add ascii art
    print('ng-py-deploy\n')
    print('Usage:')
    print('  python ng-py-deploy.py (prod | dev) [hash]')
    sys.exit()
# CM: first build the ng app
# .run shows the output during the execution
ngBuild = ['ng', 'build']
if len(sys.argv) > 1:
    if sys.argv[1] == 'prod':
        ngBuild.append('--prod')
    elif sys.argv[1] == 'dev':
        pass
    else:
        sys.exit()

print('Building...')
with open('config.json') as json_config:
    json_data = json.load(json_config)

ng_py_deploy_root = os.getcwd()
os.chdir(json_data['angular_project_root'])
result = sp.run(ngBuild)
os.chdir(ng_py_deploy_root)

if result.returncode == 0:
    # CM: get the hash
    if len(sys.argv) > 1 and sys.argv[2] == 'hash':
        print('Adding hash commit...')
        repo = '.git'
        sha = sp.check_output(['git', 'rev-parse', 'HEAD'], cwd=repo).decode('ascii').strip()
        objSlice = slice(0, 7)
        sha = sha[objSlice]

        # CM: alter index.html
        with open(json_data['angular_project_root'] + json_data['local_dir'] + json_data['base'] + '/index.html', 'r') as file:
            data = file.readlines()

        # TODO-CM: add branch name
        data[4] = '  <title>:: Commit:' + sha + '</title>\n'    # project title

        with open(json_data['angular_project_root'] + json_data['local_dir'] + json_data['base'] + '/index.html', 'w') as file:
            file.writelines( data )
        print('The hash is ' + sha)

    spCallParams = []
    if os.name == 'nt':
        spCallParams.append('bash.exe')
        spCallParams.append('-c')
    spCallParams.append('python')
    spCallParams.append('upload.py')

    result = sp.call(spCallParams, stderr=sp.DEVNULL)
    if result == 0:
        print('Process complete :D')
    else:
        print('Something fails :O')
