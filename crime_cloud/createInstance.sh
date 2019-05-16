#!/bin/bash

###################################################################
# File Name	    : createInstance.sh
# Description	: This script is used to create host variabe dnamically 
#                  and create instance usuing those variable.
# Args         	: InstanceName, VolumeName, VolumeSize
# Author       	: mtomar
###################################################################

echo "Creating $1 mounted with $2($3 GB)"

cat ./host_vars/dummyVar.yaml > ./host_vars/instanceVar.yaml
echo "instance_name: $1" >> ./host_vars/instanceVar.yaml
echo "volumes:" >> ./host_vars/instanceVar.yaml
echo "  - vol_name: $2" >> ./host_vars/instanceVar.yaml
echo "    vol_size: $3" >> ./host_vars/instanceVar.yaml

printf "\nPassword: ZjdkNDcxNDE4ODEzM2Ji\n"
. ./openrc.sh
ansible-playbook --ask-become-pass ./createInstance.yaml
