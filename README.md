# puppet-nginx-task

Automatically deploys the Puppet PSE Exercise page to a server.

This script is compatible with Ubuntu Linux servers. It has been tested
on Ubuntu 12.04 and 14.04.

Requirements: Python2 and Fabric.

To install python2 and Fabric on Ubuntu/Debian Linux flavors:
```
> sudo apt-get install python fabric
```

Fabric may also be installed via Pip:
```
> sudo pip install fabric
```

To run:

- clone this repo, cd into it, and execute the deploy_it.py script:
```
> git clone https://github.com/hacoo/puppet-nginx-task.git
> cd puppet-nginx-task
> ./deploy_it.py
```

You will be prompted to enter the IP address of the server you would like
to deploy to, and the username of a sudo-capable account on the server.
After logging in, deployment should proceed automatically. It will do the following:

- install nginx and git if necessary
- configure nginx
- pull latest changes to the webpage 
