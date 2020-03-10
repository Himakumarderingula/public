import subprocess
import xml.etree.ElementTree as ET
#import smtplib

sid = 'give your sid'
srpcommand = 'symcfg show -srp srp_1 -sid  ' + sid + ' -output xml_e'
srp_xml = subprocess.check_output(srpcommand, shell=True)
srptree = ET.fromstring(srp_xml)

### Put SRP ElementTree values into Python data structure
srpcap = dict()
#Subject= "serial no"
# Iterate through all SRP, capturing capacity information
for elem in srptree.iterfind('Symmetrix/SRP/SRP_Info'):
    #symid = elem.find('symid').text
    pool = elem.find('name').text
    totalGb = elem.find('usable_capacity_gigabytes').text
    allocGb = elem.find('allocated_capacity_gigabytes').text
    freeGb = elem.find('free_capacity_gigabytes').text
    subper = elem.find('subscribed_capacity_pct').text
    #srpcap[elem.find('symid')] = [totalGb, allocGb, freeGb]
    x=float(totalGb)

# Prettytable
from prettytable import PrettyTable
report = PrettyTable()
report.add_column("pool",[pool])
report.add_column("Usable GB",[totalGb])
report.add_column("Allocated GB", [allocGb])
report.add_column("Free GB", [freeGb])
report.add_column("Sub %", [subper])

srpcommand = 'symcfg list -srp -demand -type sl -sid ' + sid + ' -output xml_e'
snap_xml = subprocess.check_output(srpcommand, shell=True)
snaptree = ET.fromstring(snap_xml)

snapcap = dict()
for elem in snaptree.iterfind('Symmetrix/SRP/SRP_Info'):
    snapGb = elem.find('snapshots_allocated_gigabytes').text
    y=float(snapGb)

report.add_column("Snap GB",[snapGb])
snapperr=str(round((y/x)*100))
report.add_column("Snap %",[snapperr])

report.int_format = '10'
report.float_format = '10.1'
report.max_width = 60
report.format = True
print(report)
