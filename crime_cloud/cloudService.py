#!/usr/bin/env python3

import os
import subprocess

def executeScript(cmd):

    p = subprocess.Popen("bash ./createWebInstance.sh asd asd 12", stdout=subprocess.PIPE, shell=True)
 
    ## Talk with date command i.e. read data from stdout and stderr. Store this info in tuple ##
    ## Interact with process: Send data to stdin. Read data from stdout and stderr, until end-of-file is reached.  ##
    ## Wait for process to terminate. The optional input argument should be a string to be sent to the child process, ##
    ## or None, if no data should be sent to the child.
    (output, err) = p.communicate()
    
    ## Wait for date to terminate. Get return returncode ##
    p_status = p.wait()
    print ("Command output : ", output)
    

    res = subprocess.getoutput("bash %s %s %s %s" %(cmd[0], cmd[1], cmd[2], cmd[3]))
    # resp = res.communicate()
    print(res.split())
    # for line in res.stdout():
    #     print(line)
    # print (res)
    return (res)

def asd(cmd):
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    o, e = proc.communicate()

    print('Output: ' + o.decode('ascii'))
    print('Error: '  + e.decode('ascii'))
    print('code: ' + str(proc.returncode))

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
                name = input("Enter web_server name: ")
                volume = input("Enter the volume name: ")
                size = input("Enter the volume size in GB: ")

                os.system("bash ./createWebInstance.sh %s %s %s" % (name.strip(), volume.strip(), size.strip()))
                f= open("webServerInfo.txt","a")
                f.write("%s,%s,%s,"%(name.strip(), volume.strip(), size.strip()))
                f.close()
                os.system("bash ./updateWebSoft.sh %s %s")

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