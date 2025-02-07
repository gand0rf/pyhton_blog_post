import getpass
import paramiko
import time

# Setup client info
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
username = input("Username: ")
password = getpass.getpass("Password: ")

# Optional
server_ip = input("Server IP: ")
server_port = int(input("Server port: "))

# Create client conenction
client.connect(hostname=server_ip, port=server_port, username=username, password=password)

# Get hostname of remote server
stdin, stdout, stderr = client.exec_command('hostname')
server_name = stdout.read().decode().strip('\n')

print(f"Server name returned as: {server_name}")

# Get current CPU temp of remote server
stdin, stdout, stderr = client.exec_command(r"cat /sys/class/thermal/thermal_zone1/temp | sed 's/\(.\)..$/.\1°C/'")
temp = stdout.read().decode().strip('\n')

print(f'{server_name} cpu temp: {temp}')

# Get disk usage of remote machine
remote_user = input("Remote username: ")
remote_password = getpass.getpass("Remote password: ")
remote_ip = input("Remote IP: ")
remote_port = int(input("Remote port: "))

conn = client.invoke_shell()
conn.send(f'ssh {remote_user}@{remote_ip} -p {remote_port} "df | grep -v \'loop\' | grep \'dev\'"\n')
time.sleep(2)

if '(yes/no)?' in conn.recv(9999).decode():
    conn.send('yes\n')
    time.sleep(5)
    
conn.send(remote_password+'\n')
time.sleep(2)

output = conn.recv(9999).decode().split('\r')

for i in output:
    if i.split(' ')[-1] == '/':
        usage = i.split(' ')[-2]

print(f'{server_name} root usage: {usage}')