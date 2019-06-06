import os
import subprocess as sp
import sys
import re
import configparser

config = configparser.ConfigParser()
config.read('.pyngdeployrc')


def build(environment):
    ngBuild = ['ng', 'build', '--sourceMap=false']
    if environment == 'prod':
        ngBuild.append('--prod')
    elif environment == 'dev':
        pass
    else:
        sys.exit()

    print('[pyngDeploy]:: Building...')
    result = sp.run(ngBuild, shell=os.name == 'nt')
    return result


def gen_hash(generateHash, outputPath):
    if generateHash == '--hash':
        print('[pyngDeploy]:: Adding hash commit...')
        repo = f'./.git'
        sha = sp.check_output(['git', 'rev-parse', 'HEAD'],
                              cwd=repo).decode('ascii').strip()
        objSlice = slice(0, 7)
        sha = sha[objSlice]

        # CM: alter index.html
        with open(f'./{outputPath}/index.html', 'r') as file:
            data = file.readlines()

        # TODO-CM: add branch name
        replace_tag(data, 'title', sha)

        with open(f'./{outputPath}/index.html', 'w') as file:
            file.writelines(data)
        print('[pyngDeploy]:: The hash is ' + sha)


def replace_tag(data, matching_word, input_text):
    for tag in data:
        if matching_word in tag:
            splitted_tag = re.split(
                f'.+<{matching_word}>|</{matching_word}>[\r\n]', tag)
            title_text = ''.join(list(filter(None, splitted_tag)))
            data[data.index(tag)] = f"""  <{matching_word}>{title_text}
            :: Commit:{input_text}</{matching_word}>\n"""
            return
