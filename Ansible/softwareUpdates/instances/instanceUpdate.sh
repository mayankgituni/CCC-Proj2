#!/usr/bin/env bash

# . ./openrc.sh; ansible-playbook -i hosts/webHost -u ubuntu --key-file=webServer.pem --ask-become-pass webServer.yaml
. ./openrc.sh; ansible-playbook -i hosts/appHost -u ubuntu --key-file=webServer.pem --ask-become-pass appServer.yaml
# . ./openrc.sh; ansible-playbook -i hosts/dbHost -u ubuntu --key-file=webServer.pem --ask-become-pass dbServer.yaml

# Password: ZjdkNDcxNDE4ODEzM2Ji
# <App> 172.26.38.160
# <db>  172.26.37.232
# <web> 172.26.38.100
# https://ww2.fmoviesfree.net/season/silicon-valley-season-5/watching/?episode_id=36389&sv=6