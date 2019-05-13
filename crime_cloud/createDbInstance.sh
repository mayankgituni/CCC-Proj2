#!/bin/bash

read -p "Enter the db_server name: "  instName
read -p "Enter the Volume name: "  volume
echo "Creating $instName mounted with $volume"

cat ./host_vars/dummyVar.yaml > ./host_vars/instanceVar.yaml
echo "instance_name: $instName" >> ./host_vars/instanceVar.yaml
echo "volumes:" >> ./host_vars/instanceVar.yaml
echo "  - vol_name: $volume" >> ./host_vars/instanceVar.yaml
echo "    vol_size: 40" >> ./host_vars/instanceVar.yaml

printf "\nPassword: ZjdkNDcxNDE4ODEzM2Ji\n"
. ./openrc.sh
ansible-playbook --ask-become-pass ./createInstance.yaml

# echo $output > output.o