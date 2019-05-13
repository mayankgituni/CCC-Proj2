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

echo "$1 is $IP with type $fileType"
if [[ $fileType == 0 ]]; then
    echo "Building.."
    sudo docker build -t mayanktomar/webServer:$2 ./code/webServer

    echo "Login:"
    sudo docker login 

    echo "Pushing..."
    sudo docker push mayanktomar/webServer:$2

    echo "[SoftwareUpdate]" > hosts
    echo $IP >> hosts

    echo "Ansible running..."
    . ./openrc.sh; ansible-playbook -i hosts -u ubuntu --key-file=webServer.pem --ask-become-pass runContainer.yaml


    echo "Docker pulling image...."
    ssh -i webServer.pem ubuntu@$IP "sudo docker pull mayanktomar/webServer:$2"

    scp -i webServer.pem -r ./code/webServer/app/* ubuntu@$IP:/mystore

    echo "Docker running...."
    ssh -i webServer.pem ubuntu@$1 "sudo docker run --rm -v /mystore:/app -w /app -p 50000-50001:50000-50001 -d mayanktomar/webServer:$2"
else
    echo "Building.."
    sudo docker build -t mayanktomar/dbServer:$2 ./code/dbServer/

    echo "Login:"
    sudo docker login 

    echo "Pushing..."
    sudo docker push mayanktomar/dbServer:$2

    echo "[SoftwareUpdate]" > hosts
    echo $IP >> hosts

    echo "Ansible running..."
    . ./openrc.sh; ansible-playbook -i hosts -u ubuntu --key-file=webServer.pem --ask-become-pass runContainer.yaml


    echo "Docker pulling image...."
    ssh -i webServer.pem ubuntu@$IP "sudo docker pull mayanktomar/dbServer:$2"

    scp -i webServer.pem -r ./code/dbServer/app/* ubuntu@$IP:/mystore

    echo "Docker running...."
    ssh -i webServer.pem ubuntu@$1 "sudo docker run --rm -v /mystore:/app -w /app -p 50000-50001:50000-50001 -d mayanktomar/dbServer:$2"

fi

cp webServerInfo.txt code/dbServer/app/
cp dbServerInfo.txt code/webServer/app/