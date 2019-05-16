#!/usr/bin/env python3

import os
import subprocess
import re

###################################################################
# File Name	    : cloudService.sh
# Description	: This script manages the cloudService features which
#                   includes, creating instances ands updating software.
# Args         	: N/A
# Author       	: mtomar
###################################################################

'''
This method is used to take user input and create instances on the nectar cloud.
'''
def createInstance(fileName):
    name = input("Enter server name: ")
    volume = input("Enter the volume name: ")
    size = input("Enter the volume size in GB: ")
    
    if(fileName == "dbServerInfo.txt"):
        box = input("Enter the Bounding Box: ")

    # This password is used to interact with openstack
    print("Enter the password: Hint- ZjdkNDcxNDE4ODEzM2Ji")
    cmd = "ip=$(bash createInstance.sh %s %s %s);echo $ip > output.txt" % (name.strip(), volume.strip(), size.strip())
    
    # Execute the instance creation script with proper variables.
    os.system(cmd)
    fo = open("output.txt", "r")
    output = fo.readlines()

    try:
        # retrive the IP address of the new instance
        ipAddr = re.findall(r'\b(?:[0-9]{2,3}\.){3}[0-9]{1,3}\b', output[-1])[0]
    except:
        print('No IP address found!!')
        return
    
    out = "%s,%s,%s,%s\n"%(name.strip(), volume.strip(), size.strip(), ipAddr)

    print ("The instace %s is up with an IP: %s" % (name.strip(), ipAddr))
    
    if(fileName == "dbServerInfo.txt"):
        f2 = open("setup.txt","a")
        f2.write("{\"" + name.strip().split('_')[0] + "\":[" + box+"]}")
        os.system("grep %s setup.txt > ./code/dbServer/app/setup.json" % name.strip())
        f2.close()

    # Reister the instance into cloud info files.
    f= open(fileName,"a")
    f.write(out)
    f.close()

'''
This method used to build call script that build docker images, pushes
and pull on the instace and deploys the images on the volume.
'''
def updateSoftware(tagType):
    name = input("Enter name: ")
    tag = input("Enter the tag: ")

    if(tagType == 'web'):
        if(tag.strip() == ''):
            os.system("bash updateSoftware.sh %s mayanktomar/web-server:default" % (name.strip(), tag.strip()))
        else:
            os.system("bash updateSoftware.sh %s mayanktomar/web-server:%s" % (name.strip(), tag.strip()))
    else:
        os.system("grep %s setup.txt > ./code/dbServer/app/setup.json" % name.strip())
        if(tag.strip() == ''):
            os.system("bash updateSoftware.sh %s mayanktomar/db-server:default" % (name.strip(), tag.strip()))
        else:
            os.system("bash updateSoftware.sh %s mayanktomar/db-server:%s" % (name.strip(), tag.strip()))

'''
This method is used to provide interative cloud service to the user. The service may
include features such as creating an instance, updating the software and managing
cloud information.
'''
def main():
    print("*********************************************************************************************")
    print("*********************************************************************************************")
    print("*****************************--WELCOME TO THE CLOUD---***************************************")
    print("*********************************************************************************************\n")
    
    while(True):
        cmd = input("Enter command [WebServer:1, DbServer:2, CloudInfo:3, EXIT:4]: ")

        print()
        if(cmd.strip() == '1'):
            print ("-------------------------------Welcome to the Web World------------------------------")

            cmd = input("Enter command [ createInstance:1, updateSoftware:2 ]: ")

            if(cmd.strip() == '1'):
                createInstance("webServerInfo.txt")

            elif(cmd.strip() == '2'):
                updateSoftware("web")

        elif (cmd.strip()== '2'):
            print ("-------------------------------Welcome to the DB World-------------------------------")
            
            cmd = input("Enter command [ createInstance:1, updateSoftware:2 ]: ")

            if(cmd.strip() == '1'):
                createInstance("dbServerInfo.txt")

            elif(cmd.strip() == '2'):
                updateSoftware("db")

        elif (cmd.strip()== '3'):
            
            f1 = open("dbServerInfo.txt", "r")
            f2 = open("webServerInfo.txt", "r")
            print("*******--CLUSTER INFORMATION---*****************")
            print("***********--DB-SERVERS--***********************")
            for line in f1.readlines():
                print(' | '.join(line.strip().split(',')))
            
            print("\n***********--WEB-SERVERS--**********************")
            for line in f2.readlines():
                print(' | '.join(line.strip().split(',')))
            print("\n************************************************\n")
            f1.close()
            f2.close()
            
        elif (cmd.strip()== '4'):

            print("\nThank you for using the service! :-)")
            print("--------------------------------------")
            break

if __name__ == '__main__':
    main()