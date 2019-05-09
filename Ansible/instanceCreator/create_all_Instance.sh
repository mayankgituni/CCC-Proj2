#!/bin/bash

. ./openrc.sh; ansible-playbook --ask-become-pass webServer.yaml
. ./openrc.sh; ansible-playbook --ask-become-pass dbServer.yaml
. ./openrc.sh; ansible-playbook --ask-become-pass appServer.yaml

#Pass: ZjdkNDcxNDE4ODEzM2Ji