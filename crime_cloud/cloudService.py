#!/usr/bin/env python3

import os, sys
import subprocess

def executeScript(cmd):
    res = subprocess.check_output([cmd])

    # for line in res.splitlines():
    #     print(' ')

    return (res)


def main():
    print("*********************************************************************************************")
    print("*********************************************************************************************")
    print("*****************************--WELCOME TO THE CLOUD__****************************************")
    print("*********************************************************************************************\n")
    
    while(True):
        cmd = input("Enter command [WebServer:1, DbServer:2, CloudInfo:3, EXIT:4]: ")
        print()
        if(cmd.strip() == '1'):
            print ("-------------------------------Welcome to the Web World------------------------------")
            cmd = input("Enter command [createInstance:1, updateSoftware:2, GoBack:Enter]: ")

            if(cmd.strip() == '1'):
                executeScript("./web_Server/createWebInstance.sh")
                # executeScript("./db_Server/updateDbSoft.sh mayanktomar/webServer:software-V1")

            elif(cmd.strip() == '2'):
                executeScript("./db_Server/createDbInstance.sh")

        elif (cmd.strip()== '2'):
            print ("-------------------------------Welcome to the DB World-------------------------------")
            pass
        elif (cmd.strip()== '3'):
            pass
        elif (cmd.strip()== '4'):

            print("\nThank you for using the service! :-)")
            break


if __name__ == '__main__':
    main()