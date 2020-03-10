import paramiko
import time
import subprocess
import re
//IN CASE IF YOU HAVE TO EXCLUDE ASCI CODE 
ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
commands=['cmd1 && cmd2']
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('avamar.com', username='', password='')
channel = client.invoke_shell()
i=1
for command in commands:
    channel.send(command+ "\n")
    while not channel.recv_ready():
        #Wait for the server to read and respond
        time.sleep(0.1)
    if i==0:
        time.sleep(1) #wait enough for writing to (hopefully) be finished
        output1 = channel.recv(99)
        output=output1.decode('utf-8')
        while 'admin@avamarname:~/#' not in str(output.lower()):
            time.sleep(2)
            output1 = channel.recv(999)
            output=output1.decode('utf-8')
            #print(output)

     #print(line)
    #read in
        time.sleep(1)
    if i==1:
        time.sleep(1) #wait enough for writing to (hopefully) be finished
        output = channel.recv(999) #read in
        #print(output.decode('utf-8'))
        time.sleep(1)
        i=0
channel.close()
client.close()
f=open('/tmp/avamar_hc_script.txt','w')
//FOR EXCECUTING NORAML COMMANDS
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('avamar.com', username='', password='')
//below cmd is internal Avamar cmd to start health check and it will auto update the script.
stdin, stdout, stderr = client.exec_command('cd proactive_check/; yes |./proactive_check.pl')
for line in stdout:
    f.write(line)
    #print(line)
f.close()
#print(stdout)

s=''
ar=[]
f=open('/tmp/avamar_hc_script.txt','r')
email=0
for line in f:
    if 'FAILED' in line:
        #print(line)
        s2=line.replace('\n',"")
        s3=s2.replace('u\'',"")
        h=str(ansi_escape.sub('', s3))
        #line1=line.decode('utf-8')
        s=s+h
        ar.append('1')
        email=1
    if 'WARNING' in line:
        #line2=line.decode('utf-8')
        s4=line.replace('\n',"")
        s5=s4.replace('u\'',"")
        k=str(ansi_escape.sub('', s5))
        #k=str(ansi_escape.sub('', line))
        s=s+k
        ar.append('1')
        email=1

f.close()
#client.close()
if len(ar)==0:
    s='No Errors or Warnings in Proactive Health check'
f=open('/tmp/savamar1_dpn_check.txt','w')
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('avamar.lowes.com', username='', password='')
stdin, stdout, stderr = client.exec_command(' cat /home/admin/dpn_check_internaltesting.txt')
for line in stdout:
    f.write(line)
    #print(line)
f.close()
client.close()
f=open('/tmp/avamar_dpn_check.txt','r')
tm=0
for line in f:
    if 'CHECK.DPN PASSED OVERALL (prestart)' in line:
        #print(line)
        tm=1
        m='CHECK.DPN PASSED OVERALL'
f.close()
out=str('This is the Proactive Health Check Alert update')
if tm==0:
    m='CHECK.DPN NOT PASSED OVERALL, PLEASE CHECK'
    email=1
#em='"Hi All,\n\n\n "'+out+'"\n\nFrom,\nsavamar1"'
f=open('/tmp/avamar_hc_results.txt','w')
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('avamar.com', username='', password='')
stdin, stdout, stderr = client.exec_command('cd proactive_check/; cat hc_results.txt')
for line in stdout:
    line_f=str(ansi_escape.sub('', line))
    f.write(line_f)
    #print(line)
f.close()
client.close()

if email==1:
    em='"Hi All,\n\n\n This is the Proactive Health Check Alert update:-   "'+str(s)+'"\n\nThis is a status of command check.dpn --prestart:-   "'+m+'"\n\nFrom,\avamar"'
    out=subprocess.Popen('echo -e '+ em+'|mailx -a /tmp/avamar_hc_results.txt -a /tmp/avamar_dpn_check.txt -s "Avamar Proactive Health Check" -r Avamar@lowes.com userdl@lowes.com ', shell=True)
    time.sleep(35)
    subprocess.Popen.kill(out)
