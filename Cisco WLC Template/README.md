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
And creates the Host Prototypes:
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
{#AP_NAME}      matches     ^{HOST.HOST}$
```
and creates next item prototypes:
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
AP Ping
AP Receive Bytes 2.4GHz
AP Receive Bytes 5GHz
AP Transmit Bytes 2.4GHz
AP Transmit Bytes 5GHz
```
and next trigger prototypes:
```
AP CPU Load					{Template Cisco LAP:CPUUsage[{#AP_NAME}].last(#3)}>85
AP Interference Channel 2.4GHz Utilization High	{Template Cisco LAP:ap_chan_param.py["{HOST.CONN}","{#SNMPINDEX}","InterferenceUtil24","{$SNMP_COMMUNITY}"].last(#3)}>40
AP Interference Channel 5GHz Utilization High	{Template Cisco LAP:ap_chan_param.py["{HOST.CONN}","{#SNMPINDEX}","InterferenceUtil5","{$SNMP_COMMUNITY}"].last(#3)}>40
AP is unreachable				{Template Cisco LAP:icmpping[{#AP_IPADDR}].max(300)}<1
AP just been restarted				{Template Cisco LAP:cLApUpTime[{#AP_NAME}].last()}<600
AP Load Channel 2.4GHz Utilization High		{Template Cisco LAP:dot11LoadChanUtil24[{#AP_NAME}].last(#3)}>80
AP Load Channel 5GHz Utilization High		{Template Cisco LAP:dot11LoadChanUtil5[{#AP_NAME}].last(#3)}>80
AP Memory HIGH					{Template Cisco LAP:MemoryUsage[{#AP_NAME}].last(#3)}>85
AP Noise on Channel 2.4GHz is High		{Template Cisco LAP:ap_chan_param.py["{HOST.CONN}","{#SNMPINDEX}","NoisePower24","{$SNMP_COMMUNITY}"].last()}>-80
AP Noise on Channel 5GHz is High		{Template Cisco LAP:ap_chan_param.py["{HOST.CONN}","{#SNMPINDEX}","NoisePower5","{$SNMP_COMMUNITY}"].last()}>-80
MAX Clients					{Template Cisco LAP:ClientCount[{#AP_NAME}].last()}>150
Radio Interface 2.4 GHz is DOWN			{Template Cisco LAP:dot11OperStatus24[{#AP_NAME}].last()}=2
Radio Interface 5 GHz is DOWN			{Template Cisco LAP:dot11OperStatus5[{#AP_NAME}].last()}=2
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

### ap_chan_param.py
It is an external script that gets some parameters needed only on the working channel of the access point _(such as **Noise Power** or **Interference Channel Utilization**)_.
It must be placed in the external scripts directory *(usually /usr/lib/zabbix/externalscripts/)*
