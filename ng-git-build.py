import os
import subprocess as sp

# TODO-CM: add ascii art
print('Building...')
# CM: first build the ng app
# .run shows the output during the execution
result = sp.run(['ng', 'build', '--prod'], shell=True)

# CM: get the hash
if result.returncode == 0:
    print('Adding hash commit...')
    repo = '.git'
    sha = sp.check_output(['git', 'rev-parse', 'HEAD'], cwd=repo).decode('ascii').strip()
    objSlice = slice(0, 7)
    sha = sha[objSlice]
    
    # CM: alter index.html
    with open('', 'r') as file: # '' = .\\dist\\angular_project_root\\index.html
        data = file.readlines()
    
    # TODO-CM: add branch name
    data[4] = '  <title>:: Commit:' + sha + '</title>\n'    # project title
    
    with open('', 'w') as file: # '' = .\\dist\\angular_project_root\\index.html
        file.writelines( data )
    print('The hash is ' + sha)

    result = sp.call(['bash.exe', '-c', ''], stderr=sp.DEVNULL)  # '' = optional: source ~/.rcfile;  # ... python path/to/pruebas.py
    if result == 0:
        print('Process complete :D')
    else:
        print('Something fails :O')
