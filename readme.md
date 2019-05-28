# py-ng-deploy
## Install
```
pip install py-ng-deploy
```

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

>_After `init` is required to edit the .pyngdeployrc file that has the following structure:_

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
$ pyngDeploy prod hash
```
