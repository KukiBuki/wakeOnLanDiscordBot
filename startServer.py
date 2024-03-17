from distutils.dist import _CommandT
from dotenv import load_dotenv
import paramiko
import os

load_dotenv('.bobergamingenv')
boberHost=os.getenv("boberhost", default="0.0.0.0")
def startTerraria():
    
#    sshKey = paramiko.RSAKey.from_private_key_file(os.getenv("terrariauser"))
#   , pkey=sshKey
    
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=boberHost, username=os.getenv("terrariauser"))
    stdin, stdout, stderr = client.exec_command('ls -l')
    command="home/terrariaserver/.steam/steam/steamapps/common/tModLoader/DedicatedServerUtils/manage-tModLoaderServer.sh start"
    ssh_stdin, ssh_stdout, ssh_stderr = client.exec_command(command)
    
    
def startZomboid():
    
#    sshKey = paramiko.RSAKey.from_private_key_file(os.getenv("terrariauser"))
#   , pkey=sshKey    
    
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=boberHost, username=os.getenv("zomboiduser"))
    stdin, stdout, stderr = client.exec_command('ls -l')
    command="home/terrariaserver/.steam/steam/steamapps/common/tModLoader/DedicatedServerUtils/manage-tModLoaderServer.sh start"
    ssh_stdin, ssh_stdout, ssh_stderr = client.exec_command(command)