#!/bin/bash

# <IP> <Port> <ImageName> 172.26.38.181 50000-50001:50000-50001 mayanktomar/testing:flasking

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

# echo "Building.."
# sudo docker build -t $3 ./code

# echo "Login:"
# sudo docker login 

# echo "Pushing..."
# sudo docker push $3

# echo "[SoftwareUpdate]" > hosts
# echo $1 >> hosts

# echo "Ansible running..."
# . ./openrc.sh; ansible-playbook -i hosts -u ubuntu --key-file=webServer.pem --ask-become-pass runContainer.yaml


# echo "Docker pulling image...."
# ssh -i webServer.pem ubuntu@$1 "sudo docker pull $3"

# scp -i webServer.pem -r ./code/app/* ubuntu@$1:/mystore

# echo "Docker running...."
# # ssh -i webServer.pem ubuntu@$1 "sudo docker run -p $2 -d $3"
# ssh -i webServer.pem ubuntu@$1 "sudo docker run --rm -v /mystore:/app -w /app -p 50000-50001:50000-50001 -d $3"
# #ZjdkNDcxNDE4ODEzM2Ji