#!/bin/bash

# <IP> <Port> <ImageName>
echo "Building.."
sudo docker build -t $3 ./code

echo "Login:"
sudo docker login 

echo "Pushing..."
sudo docker push $3

echo "[uploadContainer]" > hosts
echo $1 >> hosts

echo "Ansible running..."
. ./openrc.sh; ansible-playbook -i hosts -u ubuntu --key-file=webServer.pem --ask-become-pass runContainer.yaml


echo "Docker pulling image...."
ssh -i webServer.pem ubuntu@$1 "sudo docker pull $3"

echo "Docker running...."
ssh -i webServer.pem ubuntu@$1 "sudo docker run -v /mystore:/app -p $2 -d $3"
