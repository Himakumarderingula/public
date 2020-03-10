import paramiko
import xml.etree.ElementTree as ET
import subprocess
import time
import os
//connecting to avamar servers
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('', username='admin', password='')
stdin, stdout, stderr = client.exec_command('mccli activity show all --verbose=true --xml')
f = open('/root/output.xml', 'w')
for line in stdout:
     f.write(line)
f.close()
client.close()
//Function to connect to servers
def client_connect(cmd):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect('', username='admin', password='')
    stdin, stdout, stderr = client.exec_command(cmd)
    time.sleep(30)
    client.close()
    return
//Parsing the coped data from file
tree = ET.parse('/root/output.xml')
root = tree.getroot()
for elem in root.iterfind('Data/Row'):
    session_id=elem.find('ID').text
    client_name = elem.find('Client').text
    status = elem.find('Status').text
    elapsed= elem.find('Elapsed').text
    error_code=elem.find('ErrorCode').text
    plugin=elem.find('Plug-In').text
    domain=elem.find('Domain').text
    if status == 'Waiting-Client':
        if plugin not in ('Windows VMware Image','Linux VMware Image','Replicate'):
            et=elapsed.split(':')
            h=et[0]
            m=et[1]
            hr=(int(h[:-1]))*60
            mi=int(m[:-1])
            time_elp=hr+mi
            print('Elapsed min is',time_elp,client_name)
            if time_elp>30:
                rawPingFile = os.popen('ping -c 5 %s' % (client_name))
                rawPingData = str(rawPingFile.readlines())
                if rawPingData=='[]':
                    cancel_cmd='mccli activity cancel --id='+session_id
                    disable_cmd='mccli client edit --domain='+domain+' --name='+client_name+' --enabled=false'
                    client_connect(cancel_cmd)
                    client_connect(disable_cmd)
                    out=subprocess.Popen('echo '+client_name+' Waiting time is '+elapsed+', it seems server is decommissioned or renamed  hence Backup has been cancelled and disabled. Kindly investigate further.''|mailx -s'+client_name+'" Backup Status" -r ', shell=True)
                    time.sleep(30)
                    subprocess.Popen.kill(out)
                else:
                    lost = rawPingData.split('received, ')[1].split(' ')[0]
                    partiaPing=int(lost.split('%')[0])
                    if lost=='0%':
                        out=subprocess.Popen('echo '+client_name+' Waiting time is '+elapsed+' Seems connectivity is working fine, need your intervention. Kinldy check Avamar Backup service status. ''|mailx -s'+client_name+'" Backup Status" -r ', shell=True)
                        time.sleep(30)
                        subprocess.Popen.kill(out)
                    if lost=='100%':
                        cancel_cmd='mccli activity cancel --id='+session_id
                        client_connect(cancel_cmd)
                        out=subprocess.Popen('echo '+client_name+' Waiting time is '+elapsed+' Unable to ping client, some connectivity issue is there. Backup has been cancelled for now, Please investigate further.''|mailx -s'+client_name+'" Backup Status" -r ', shell=True)
                        time.sleep(30)
                        subprocess.Popen.kill(out)
                    if partiaPing in range(1,99):
                        out=subprocess.Popen('echo '+client_name+' Waiting time is '+elapsed+' There is an intermittent conntivity issue,'+rawPingData+' please investigate further''|mailx -s'+client_name+'" Backup Status" -r ', shell=True)
                        time.sleep(30)
                        subprocess.Popen.kill(out)

