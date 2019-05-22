import os
import subprocess as sp
import sys
import json

json_data = {}
with open('config.json') as json_config:
    json_data = json.load(json_config)

def build(environment):
    ngBuild = ['ng', 'build']
    if environment == 'prod':
        ngBuild.append('--prod')
    elif environment == 'dev':
        pass
    else:
        sys.exit()

    print('Building...')

    ng_py_deploy_root = os.getcwd()
    os.chdir(json_data['angular_project_root'])
    result = sp.run(ngBuild)
    os.chdir(ng_py_deploy_root)
    return result

def gen_hash(generateHash):
    if generateHash == 'hash':
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
