import os
import subprocess as sp
import sys
import json

# TODO-CM: add ascii art
print('Building...')
# CM: first build the ng app
# .run shows the output during the execution
ngBuild = ['ng', 'build']
if len(sys.argv) > 1 and sys.argv[1] == 'prod':
    ngBuild.append('--prod')

with open('config.json') as json_config:
    data = json.load(json_config)

result = sp.run(ngBuild)

if result.returncode == 0:
    # CM: get the hash
    if len(sys.argv) > 1 and sys.argv[2] == 'hash':
        print('Adding hash commit...')
        repo = '.git'
        sha = sp.check_output(['git', 'rev-parse', 'HEAD'], cwd=repo).decode('ascii').strip()
        objSlice = slice(0, 7)
        sha = sha[objSlice]

        # CM: alter index.html
        with open(data['index_path'], 'r') as file:
            data = file.readlines()

        # TODO-CM: add branch name
        data[4] = '  <title>:: Commit:' + sha + '</title>\n'    # project title

        with open(data['index_path'], 'w') as file:
            file.writelines( data )
        print('The hash is ' + sha)

    spCallParams = []
    if os.name == 'nt':
        spCallParams.append('bash.exe')
        spCallParams.append('-c')
    # if os.name == 'posix':
    #     spCallParams.append(f'python {data["upload_py_path"]}')
    spCallParams.append('python')
    spCallParams.append(f'{data["upload_py_path"]}')    # '' = optional: source ~/.rcfile;  # ... python /relative/path/to/pruebas.py

    result = sp.call(spCallParams, stderr=sp.DEVNULL)
    # result = sp.call(spCallParams)
    if result == 0:
        print('Process complete :D')
    else:
        print('Something fails :O')
