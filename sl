#!/usr/bin/python

from sloth.api import main

default_server_config_file = '/etc/sloth/server.conf'
default_config_file = '/etc/sloth/default.conf'

main(default_server_config_file, default_config_file)