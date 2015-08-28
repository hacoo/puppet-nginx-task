#! /usr/bin/env python

# Henry Cooney <hacoo36@gmail.com> <Github: hacoo>
#
# Automatically deploys the Puppet Labs PSE Exercise
# web page to a server.

import sys
from fabric.context_managers import settings
from fabfile import deploy

ip = raw_input("Enter deployment IP: ")
username = raw_input("Enter username: ")

with(settings(host_string="%s@%s" % (username, ip))):
    deploy()








