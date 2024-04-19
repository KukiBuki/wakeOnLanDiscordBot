import string
from  bobergamingenv import *
import paramiko
import sys

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

def startTerraria() -> str:
    
    command="nohup /home/terrariaserver/.steam/steam/steamapps/common/tModLoader/DedicatedServerUtils/manage-tModLoaderServer.sh start 1>/dev/null 2>/dev/null &"
    ssh_stdin = ssh_stdout = ssh_stderr = None
    
    try:
       client.connect(hostname=boberHost, username=terrariaUser)
       ssh_stdin, ssh_stdout, ssh_stderr = client.exec_command(command)
       ssh_stdout.channel.recv_exit_status()
       ssh_stdin.close()
       client.close()
    
    except Exception as e:
       sys.stderr.write("SSH connection error: {0}".format(e))
    
    if ssh_stdout:
       sys.stdout.write(ssh_stdout.read().decode("UTF-8"))
    if ssh_stderr:
       sys.stderr.write(ssh_stderr.read().decode("UTF-8"))
       
    return 'Terraria server started'


def startZomboid() -> str:
    
    command="nohup /home/pzserver/pzserver start 1>/dev/null 2>/dev/null &"
    ssh_stdin = ssh_stdout = ssh_stderr = None
    
    try:
        client.connect(hostname=boberHost, username=zomboidUser)
        ssh_stdin, ssh_stdout, ssh_stderr = client.exec_command(command)
        ssh_stdout.channel.recv_exit_status()
        ssh_stdin.close()
        client.close()
    
    except Exception as e:
        sys.stderr.write("SSH connection error: {0}".format(e))

    if ssh_stdout:
        sys.stdout.write(ssh_stdout.read().decode("UTF-8"))
    if ssh_stderr:
        sys.stderr.write(ssh_stderr.read().decode("UTF-8"))
    
    return 'Terraria server started'

