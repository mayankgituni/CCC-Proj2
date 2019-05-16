#!/bin/bash

###################################################################
# File Name	    : updateSoftware.sh
# Description	: # This script is used to create new builds and 
#                   deply softwares on the nectar cloud.
# Args         	: InstanceName, tagName
# Author       	: mtomar
###################################################################

# Identifies the IP address and type of the instance that uses has input.
grep $1 webServerInfo.txt
if [[ $? == 0 ]]; then
    grep "$1," webServerInfo.txt > out
    IP=$(grep -oE '\d+\.\d+\.\d+\.\d+' out)
    rm out
    fileType=0
else
    grep $1 dbServerInfo.txt
    if [[ $? == 0 ]]; then
        fileType=1
        grep "$1," dbServerInfo.txt > out
        IP=$(grep -oE '\d+\.\d+\.\d+\.\d+' out)
        rm out
        
    else
        fileType=1123
        echo "IP not found."
        exit $exit_code
    fi
fi

# update the information of the cloud which later sent to the instance
cp webServerInfo.txt dbServerInfo.txt code/dbServer/app/
cp webServerInfo.txt dbServerInfo.txt code/webServer/app/

echo "$1 is $IP with type $fileType"
echo "Building.."

echo "Loading the software on the /mystore"
ssh -i webServer.pem ubuntu@$IP "sudo chmod ugo+rwx /mystore"

if [[ $fileType == 0 ]]; then
    sudo docker build -t $2 ./code/webServer/
    scp -i webServer.pem -r ./code/webServer/app/* ubuntu@$IP:/mystore/
else
    sudo docker build -t $2 ./code/dbServer/
    scp -i webServer.pem -r ./code/dbServer/app/* ubuntu@$IP:/mystore
fi

echo "Docker Login:"
sudo docker login 

echo "Pushing the docker image..."
sudo docker push $2

echo "[SoftwareUpdate]" > hosts
echo $IP >> hosts

echo "Ansible running... Hint key[ ZjdkNDcxNDE4ODEzM2Ji ] "
. ./openrc.sh
ansible-playbook -i hosts -u ubuntu --key-file=webServer.pem --ask-become-pass updateServerSoftware.yaml

echo "Pulling docker image...."
ssh -i webServer.pem ubuntu@$IP "sudo docker pull $2"

echo "Stopping all the containers...."
ssh -i webServer.pem ubuntu@$IP "sudo docker kill $(sudo docker ps -q)"

echo "Docker new image deployed...."
if [[ $fileType == 0 ]]; then
    ssh -i webServer.pem ubuntu@$IP "sudo docker run -p 50002:5984 -v /mystore/data:/opt/couchdb/data -d couchdb:2.3.0 --ip=192.168.0.1"
fi
ssh -i webServer.pem ubuntu@$IP "sudo docker run -v /mystore:/app -w /app -p 50000-50001:50000-50001 -d $2"