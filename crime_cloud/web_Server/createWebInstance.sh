#!/bin/bash

read -p "Enter the instance Name: "  instName
echo "Creating $instName"

cat ./host_vars/dummyVar.yaml > ./host_vars/instanceVar.yaml
echo "instance_name: $instName" >> ./host_vars/instanceVar.yaml

echo "Password: ZjdkNDcxNDE4ODEzM2Ji"
. ./openrc.sh;output=$(ansible-playbook --ask-become-pass createInstance.yaml)

echo $output > output.o