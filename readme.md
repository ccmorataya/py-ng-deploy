# py-ng-deploy

## Requirements
* node
* angular-cli
* python3

## Install
**_Recomended_**
```
pip install py-ng-deploy
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
Shows version, simple usage and notify if the actual folder doesn't has an rc file.
```
$ pyngDeploy
```

> **NOTE** `pyngDeploy` needs to be runned inside the angular project

### Initialize project
```
$ pyngDeploy init
```

>_After `init` is required to edit the .pyngdeployrc file with the following structure:_

```ini
[dev]
Host = localhost
Username = user
Password = pass
RemoteDir = /remote/dir/path

[prod]
Host = localhost
Username = user
Password = pass
RemoteDir = /remote/dir/path
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
$ pyngDeploy dev --hash
```

### Restore last backup
```
$ pyngDeploy dev --restore
```

## TODO
- [X] Avoid leaving `None` the `cnopts.hostKeys`
- [X] Change rcfile to configuration file (.ini)
- [X] Add colors to `pyngDeploy` messages
- [X] Add check for .pyngdeployrc when `pyngDeploy` is lauched and send warning
- [X] Improve upload integration from Windows to Linux
- [X] Add `Port` key in .pyngdeployrc and read it
- [ ] Add flag `--skip-build`
