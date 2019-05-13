#!/bin/bash

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

cp webServerInfo.txt code/dbServer/app/
cp dbServerInfo.txt code/webServer/app/

echo "$1 is $IP with type $fileType"
echo "Building.."

if [[ $fileType == 0 ]]; then
    sudo docker build -t $2 ./code/webServer/
else
    sudo docker build -t $2 ./code/dbServer/
fi

echo "Login:"
sudo docker login 

echo "Pushing..."
sudo docker push $2

echo "[SoftwareUpdate]" > hosts
echo $IP >> hosts

echo "Ansible running... Hint key[ ZjdkNDcxNDE4ODEzM2Ji ] "
. ./openrc.sh
ansible-playbook -i hosts -u ubuntu --key-file=webServer.pem --ask-become-pass updateServerSoftware.yaml

echo "Loading the software on the /mystore"
ssh -i webServer.pem ubuntu@$IP "sudo chmod ugo+rwx /mystore"
scp -i webServer.pem -r ./code/webServer/app/* ubuntu@$IP:/mystore

echo "Docker pulling image...."
ssh -i webServer.pem ubuntu@$IP "sudo docker pull $2"

echo "Stopping all the containers...."
ssh -i webServer.pem ubuntu@$IP "sudo docker kill $(sudo docker ps -q)"

echo "Docker running...."
ssh -i webServer.pem ubuntu@$IP "sudo docker run --rm -v /mystore:/app -w /app -p 50000-50001:50000-50001 -d $2"