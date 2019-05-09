#!/bin/bash

. ./openrc.sh; ansible-playbook -i hosts -u ubuntu --key-file=keys/webServer.pem nectar.yaml