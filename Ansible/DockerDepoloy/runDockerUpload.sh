#!/bin/bash

# <IP> <Port> <ImageName> 172.26.38.181 50000-50001:50000-50001 mayanktomar/testing:flasking
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

scp -i webServer.pem -r ./code/app/* ubuntu@$1:/mystore

echo "Docker running...."
# ssh -i webServer.pem ubuntu@$1 "sudo docker run -p $2 -d $3"
ssh -i webServer.pem ubuntu@$1 "sudo docker run --rm -v /mystore:/app -w /app -p $2 -d $3"
#ZjdkNDcxNDE4ODEzM2Ji