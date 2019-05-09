#!/usr/bin/env bash

. ./openrc.sh; ansible-playbook -i hosts/webHost -u ubuntu --key-file=webServer.pem --ask-become-pass webServer.yaml
. ./openrc.sh; ansible-playbook -i hosts/appHost -u ubuntu --key-file=webServer.pem --ask-become-pass appServer.yaml
. ./openrc.sh; ansible-playbook -i hosts/dbHost -u ubuntu --key-file=webServer.pem --ask-become-pass dbServer.yaml