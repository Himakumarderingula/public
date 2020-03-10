import paramiko
from datetime import datetime
import time
#import getpass
import subprocess
files_creation_time=str(datetime.now().strftime('%Y_%b_%d_%Hh_%Mm_%Ss_%ffs'))
host=''
ip=''
port=22
#username=''
#password=''
userlogin_email=subprocess.Popen('echo '+username+' is executing script ''|mail -s" Backup Status", "email"', shell=True)
time.sleep(20)
subprocess.Popen.kill(userlogin_email)


def remote(command):
    ssh=paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip,port,username,password)
    stdin,stdout,stderr=ssh.exec_command(command)
    node_output=str(stdout.readlines())
    ssh.close()
    return(node_output)
def remote_reclaim(command):
    answer = 'y'
    ssh1=paramiko.SSHClient()
    ssh1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh1.connect(ip,port,username,password)
    stdin,stdout,stderr=ssh1.exec_command(command)
    stdin.write(answer + '\n')
    time.sleep(5)
    node1_output=str(stdout.readlines())
    ssh.close()
    return(node1_output)
//check to server is active or not
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('', username='', password='') 
#host = str(input('Enter server name to be reclaimed \n'))
output=str(subprocess.Popen(["ping","-c1", host],stdout=subprocess.PIPE).communicate()[0])
print(output,host)

client.close()
if output=='': 
    ali_details=''
    file1=open('aliout_'+files_creation_time+'.txt','w')
    #print ("Server Decommed",host)
    ssh=paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip,port,username,password)
    print('Executing command alishow '+host+'*')
    stdin,stdout,stderr=ssh.exec_command('alishow '+host+'*')
    ali_output=str(stdout.readlines())
    print('ali_output\n ',ali_output)
    for line in ali_output:
        file1.write(line)
        print(line)
    file1.close()
    file2=open('aliout_'+files_creation_time+'.txt','r')
    ali_name=[]
    ali_notfound=1
    for line in file2:
        for split0 in line.split('\\t'):
            for split1 in split0.split('alias:'):
                for split2 in split1.split('\\n'):
                    for split3 in split2.split('[u'):
                        for split4 in split3.split('u\''):
                            for split5 in split4.split('\''):
                                for split6 in split5.split(','):
                                    for split7 in split6.split(']'):
                                        for split8 in split7.split( ):
                                            if host in split8:
                                                ali_name.append(split8)
                                                ali_rem= 'alidelete '+ split8
                                                ali_details= ali_details +ali_rem+' && '
                                                ali_notfound=0
                                            else: 
                                                print('no alias found, script terminated. Please check for ali details')
                                                ali_notfound=ali_notfound+1

    file2.close()

nodefind_count=[]
zoing_cmd1=[]
zoing_cmd2=[]
zoing_cmd3=[]
count_config1=0
count_config2=0
count_config3=0
def count_nodefind(i):
    nodefind_count.append(i)
    return
number_of_alias=len(ali_name)
i=0
j=1
print('\nlist of Alias present for '+host+' are '+ str(ali_name))
while j<=number_of_alias:
    server_hba=ali_name[i]
    ssh=paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip,port,username,password)
    stdin,stdout,stderr=ssh.exec_command('nodefind '+server_hba)
    node_details=str(stdout.readlines())
    ssh.close()
    if 'No device found' in node_details:
        count_nodefind(i)
        print('No device found for HBA\'S',node_details)
    else:
        print('There are some active devices for '+server_hba)
    i=i+1
    j=j+1

def cfgrem1(h):
    zoing_cmd1.append(h)
    return   
def cfgrem2(k):
    zoing_cmd2.append(k)
    return   
def cfgrem3(l):
    zoing_cmd3.append(l)
    return      
if number_of_alias==len(nodefind_count) and ali_notfound==0 :
    
    total_cmd1=''
    total_cmd2=''
    total_cmd3=''
    cmd1=remote('cfgshow group | grep -i '+host)
    if host in cmd1:
    
        f = open('cmd1_'+files_creation_time+'.txt','w')
        for line in cmd1:
            f.write(line)
        f.close()
        f=open('cmd1_'+files_creation_time+'.txt','r')
        for line in f:
            for split0 in line.split(';'):
                for split1 in split0.split('\\n'):
                    for split2 in split1.split('\''):
                        for split3 in split2.split(','):
                            for split4 in split3.split('u'):
                                for split5 in split4.split('\\t'):
                                    for split6 in split5.split('['):
                                        for split7 in split6.split(']'):
                                            for split8 in split7.split( ):
                                                print(split8)
                                                if host in split8:
                                                    cfg_rem_cmd='cfgremove ,'+split8
                                                    zone_delete_cmd='zonedelete '+split8
                                                    total_cmd1=total_cmd1+cfg_rem_cmd+' && '+ zone_delete_cmd+ ' && '
                                                    #print('Executing command'+'cfgremove SADTQ_ODD,'+split8)
                                                    
                                                    #print(cfg_remove)
                                                    #zone_delete=remote('Zonedelete '+split8)
                                                    #print(zone_delete)
                                                if host not in split8:
                                                    cfgrem1('1')
                                                    print('There is some error occured in host name retrival, please check the script')
                                                    
        f.close()
    else:
        print('No configurations present')
        count_config1=count_config1+1
        
    cmd2=remote('cfgshow group | grep -i '+host)
    if host in cmd2:
        f = open('cmd2_'+files_creation_time+'.txt','w')
        for line in cmd2:
            f.write(line)
        f.close()
        f=open('cmd2_'+files_creation_time+'.txt','r')
        for line in f:
            for split0 in line.split(';'):
                for split1 in split0.split('\\n'):
                    for split2 in split1.split('\''):
                        for split3 in split2.split(','):
                            for split4 in split3.split('u'):
                                for split5 in split4.split('\\t'):
                                    for split6 in split5.split('['):
                                        for split7 in split6.split(']'):
                                            for split8 in split7.split( ):
                                                print(split8)
                                                if host in split8:                   
                                                    cfg_rem_cmd='cfgremove group,'+split8
                                                    zone_delete_cmd='zonedelete '+split8
                                                    total_cmd2=total_cmd2+cfg_rem_cmd+ ' && '+ zone_delete_cmd+ ' && ' 
                                                    #print('Executing command'+'cfgremove SADTQ_ODD_DR_TEST,'+split8)
                                                    #cfg_remove=remote('cfgremove SADTQ_ODD_DR_TEST,'+split8)
                                                    #print(cfg_remove)
                                                    #zone_delete=remote('Zonedelete '+split8)
                                                    #print(zone_delete)
                                                 
                                                if host not in split8:
                                                    cfgrem2('1')
                                                    print('There is some error occured in host name retrival, please check the script')
        f.close()
    else:
        print('No configurations present')
    cmd3=remote('cfgshow group | grep -i '+host)
    if host in cmd3:    
        f = open('cmd3_'+files_creation_time+'.txt','w')
        for line in cmd3:
            f.write(line)
        f.close()
        f=open('cmd3_'+files_creation_time+'.txt','r')
        for line in f:
            for split0 in line.split(';'):
                for split1 in split0.split('\\n'):
                    for split2 in split1.split('\''):
                        for split3 in split2.split(','):
                            for split4 in split3.split('u'):
                                for split5 in split4.split('\\t'):
                                    for split6 in split5.split('['):
                                        for split7 in split6.split(']'):
                                            for split8 in split7.split( ):
                                                print(split8)
                                                if host in split8:
                                                    cfg_rem_cmd='cfgremove SR,'+split8
                                                    zone_delete_cmd='zonedelete '+split8
                                                    total_cmd3=total_cmd3+cfg_rem_cmd+ ' && '+ zone_delete_cmd+ ' && '
                                                    #print('Executing command'+'cfgremove SADTQ_ODD_FULL_DR,'+split8)
                                                    #cfg_remove=remote('cfgremove SADTQ_ODD_FULL_DR,'+split8 ' && cfgsave)
                                                    #print(cfg_remove)
                                                    #zone_delete=remote('Zonedelete '+split8, '&& 
                                                    #rint(zone_delete)
                                             
                                                if host not in split8:
                                                    cfgrem3('1')
                                                    print('There is some error occured in host name retrival, please check the script')
        f.close()
    else:
        print('No configurations present')
    k=1
    l=0
    
    if len(zoing_cmd1)==0 and len(zoing_cmd2)==0 and len(zoing_cmd3)==0 and ali_notfound==0:
        yes = set(['yes','y'])
        no = set(['no','n'])
        print('Executing command \n'+total_cmd1 +' cfgsave \n')
        print('Executing command \n'+total_cmd2 +' cfgsave\n')
        print('Executing command \n'+total_cmd3 +' cfgsave\n')
        print('Executing command \n'+ali_details+'cfgsave\n')
        z=0
        while z<1:
            choice = input('Do you want to proceed with Command Execution(yes, y, no, n)').lower()
            if choice in yes:
                z=z+1
                commd1=total_cmd1 +'cfgsave'
                commd1_out=remote_reclaim(commd1)
                print(commd1_out)
                time.sleep(10)
                commd2=total_cmd2 +'cfgsave'
                commd2_out=remote_reclaim(commd2)
                print(commd2_out)
                time.sleep(10)
                commd3=total_cmd3 +'cfgsave'
                commd3_out=remote_reclaim(commd3)
                print(commd3_out)
                time.sleep(10)
                print('list of alias',ali_name)
        #while k<=number_of_alias:
            #server_hba=str(ali_name[l])
                ad=ali_details+'cfgsave'
                ali_delete=remote_reclaim(ad)
                print(ali_delete)
                print('Alias '+str(ali_name)+' has been deleted')
            if choice in no:
                z=2
                print('Exiting from the script as you have choosen no')
            if choice not in ['yes','y','no','n']:
                print('Please choose correct option')
            
            
            #k=k+1
            #l=l+1
        
    if len(zoing_cmd1)>0 or len(zoing_cmd2)>0 or len(zoing_cmd3)>0:
        print('error occured in configuration!!! Not a Single Reclamation step executed please check and re-run the script!!!')

userlogout_email=subprocess.Popen('echo script execution completed by '+username+' ''|mail -s" Backup Status", "email.com"', shell=True)
time.sleep(20)
subprocess.Popen.kill(userlogout_email)


