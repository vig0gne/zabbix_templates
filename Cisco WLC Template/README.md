# zabbix_templates
## Cisco WLC Template

Template for automatic discovery LAPs, creation of host prototypes and assigning the template to its.

### Cisco_WLC_Template.xml
It is template assigned to WLC.

Required MIBs: 
[CISCO-LWAPP-AP-MIB](https://circitor.fr/Mibs/Html/C/CISCO-LWAPP-AP-MIB.php) & [CISCO-LWAPP-AP-EXT-MIB](https://www.circitor.fr/Mibs/Html/C/CISCO-LWAPP-EXT-MIB.php) & [AIRESPACE-WIRELESS-MIB](http://www.circitor.fr/Mibs/Html/A/AIRESPACE-WIRELESS-MIB.php)

It has one Discovery Rule with two macroses:
```
discovery[{#AP_NAME},bsnAPName,{#AP_GROUP},bsnAPGroupVlanName]
```
Filtered with filter rule so that only already configured access points get in. 
*Change it for your filter*
```
{#AP_NAME}    matches     ^\w{2}-.+$
```
And creates the Host Prototypes:
*I've one group only, but you can use different*
```
Host name: {#AP_NAME}
Groups: 'Cisco LAP'
Group prototypes: Cisco LAP/{#AP_GROUP}
```

### Cisco_LAP_templates.xml
It is template assigned to the host prototypes in previous discovery proccess.
It has one Discovery Rule with two macroses used in item prototypes:
```
discovery[{#AP_NAME},bsnAPName,{#AP_IPADDR},bsnApIpAddress]
```
but it has one filter rule:
```
{#AP_IPADDR}    don't match  0.0.0.0
{#AP_NAME}      matches      ^{HOST.HOST}$
```
and creates next two master items:
```
**AP Channel Info (Master)**
**AP Hw Resources (Master)**
```
and next dependent items:
```
AP Channel 2.4GHz
AP Channel 5GHz
AP Client Count
AP CPU Usage
AP Interference Channel Utilization 2.4GHz
AP Interference Channel Utilization 5GHz
AP Joined Time
AP Load Channel Utilization 2.4GHz
AP Load Channel Utilization 5GHz
AP Memory Usage
AP Noise Power 2.4GHz
AP Noise Power 5GHz
AP Operational Status 2.4GHz
AP Operational Status 5GHz
AP Receive Bytes 2.4GHz
AP Receive Bytes 5GHz
AP Transmit Bytes 2.4GHz
AP Transmit Bytes 5GHz
```
and just simple check item:
```
AP Ping
```
and next trigger prototypes:
```
AP CPU Load					                    last(/Template Cisco LAP/CPUUsage[{#AP_NAME}])>85
AP Interference Channel 2.4GHz Utilization High	min(/Template Cisco LAP/dot11ChanInterference2G.[{#AP_NAME}],600s)>40
AP Interference Channel 5GHz Utilization High	min(/Template Cisco LAP/dot11ChanInterference5G.[{#AP_NAME}],600s)>40
AP is unreachable				                max(/Template Cisco LAP/icmpping[{#AP_IPADDR}],300s)<1
AP just been rejoined				            last(/Template Cisco LAP/cLApUpTime[{#AP_NAME}])<600
AP Load Channel 2.4GHz Utilization High		    min(/Template Cisco LAP/dot11LoadChanUtil24[{#AP_NAME}],600s)>80
AP Load Channel 5GHz Utilization High		    min(/Template Cisco LAP/dot11LoadChanUtil5[{#AP_NAME}],600s)>80
AP Memory HIGH					                avg(/Template Cisco LAP/MemoryUsage[{#AP_NAME}],#3)>85
AP Noise on Channel 2.4GHz is High		        min(/Template Cisco LAP/dot11ChanNoise2G.[{#AP_NAME}],300s)>-80
AP Noise on Channel 5GHz is High		        min(/Template Cisco LAP/dot11ChanNoise5G.[{#AP_NAME}],300s)>-80
MAX Clients					                    last(/Template Cisco LAP/ClientCount[{#AP_NAME}])>25
Radio Interface 2.4 GHz is DOWN			        last(/Template Cisco LAP/dot11OperStatus24[{#AP_NAME}])<>1
Radio Interface 5 GHz is DOWN			        last(/Template Cisco LAP/dot11OperStatus5[{#AP_NAME}])<>1
```
and next graph prototypes:
```
{#AP_NAME} Associated Clients
{#AP_NAME} CPU Usage
{#AP_NAME} Load Channel Utilization
{#AP_NAME} Memory Usage
{#AP_NAME} Noise Power
{#AP_NAME} Traffic on Radio Modules
```