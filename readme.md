# py-ng-deploy

## Requirements
* node
* angular-cli
* python3

## Install
**_Recomended_**
```
pip install -i https://test.pypi.org/simple/ py-ng-deploy
```
**_Alternative_**
* Clone this repo:  
`$ git clone https://github.com/ccmorataya/py-ng-deploy.git`
* Change dir to _py-ng-deploy:_  
`$ cd py-ng-deploy`
* Install with _setup.py:_  
`$ python setup.py install`

## Usage
### Info
```
$ pyngDeploy
```

> **NOTE** `pyngDeploy` needs to be runned inside the angular project

### Initialize project
```
$ pyngDeploy init
```

>_After `init` is required to edit the .pyngdeployrc file with the following structure:_

```json
{
    "host": "localhost",
    "username": "user",
    "password": "pass",
    "remote_dir": "/remote/dir/path"
}
```

> **Remember to exclude the `.pyngdeployrc` file from git**

### Build and upload (development)
```
$ pyngDeploy dev
```

### Build and upload (production)
```
$ pyngDeploy prod
```

### Build with hash in `<title>` and upload (development)
```
$ pyngDeploy dev hash
```

### Restore last backup
```
$ pyngDeploy restore
```

## TODO
- [X] Avoid leaving `None` the `cnopts.hostKeys`
- [ ] Improve upload integration from Windows to Linux _(Actually not working)_
