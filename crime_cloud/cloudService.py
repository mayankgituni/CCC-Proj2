#!/usr/bin/env python3

import os
import subprocess
import re

def createInstance(fileName):
    name = input("Enter server name: ")
    volume = input("Enter the volume name: ")
    size = input("Enter the volume size in GB: ")
    
    if(fileName == "dbServerInfo.txt"):
        box = input("Enter the Bounding Box: ")

    print("Enter the password: Hint- ZjdkNDcxNDE4ODEzM2Ji")
    cmd = "ip=$(bash createWebInstance.sh %s %s %s);echo $ip > output.txt" % (name.strip(), volume.strip(), size.strip())
    
    os.system(cmd)
    
    fo = open("output.txt", "r")
    output = fo.readlines()
    
    try:
        ipAddr = re.findall(r'\b(?:[0-9]{2,3}\.){3}[0-9]{1,3}\b', output[-1])[0]
    except:
        return
    
    out = "%s,%s,%s,%s\n"%(name.strip(), volume.strip(), size.strip(), ipAddr)
    print ("The instace %s is up with an IP: %s" % (name.strip(), ipAddr))
    f= open(fileName,"a")

    if(fileName == "dbServerInfo.txt"):
        f2 = open(name+".setup","w")
        f2.write(box)
        os.system("mv "+name+".setup "+ "./code/dbServer/app")
        f2.close()

    f.write(out)
    f.close()

def updateSoftware(tagType):
    name = input("Enter name: ")
    tag = input("Enter the tag: ")
    if(tagType == 'web'):
        os.system("bash updateSoftware.sh %s mayanktomar/web-server:%s" % (name.strip(), tag.strip()))
    else:
        os.system("bash updateSoftware.sh %s mayanktomar/db-server:%s" % (name.strip(), tag.strip()))

def main():
    print("*********************************************************************************************")
    print("*********************************************************************************************")
    print("*****************************--WELCOME TO THE CLOUD---****************************************")
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