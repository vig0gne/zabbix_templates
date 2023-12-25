#!/usr/bin/python3
"""
List of parameters
:param arg[1] - Controller Address
:param arg[2] - AP Index
:param arg[3] - Case
:param arg[4] - SNMP Community
"""

import os
from snmp_cmds import *
import sys

os.environ['MIBS'] = 'AIRESPACE-WIRELESS-MIB'
# args = sys.argv
args = ['test', '10.45.200.200', '112.107.185.129.146.224', 'NoisePower5', 'NfRcBrJvV']
query = Session(ipaddress=args[1], read_community=args[4], timeout=10)
interferencemib = 'AIRESPACE-WIRELESS-MIB::bsnAPIfInterferenceUtilization.'
noisemib = 'AIRESPACE-WIRELESS-MIB::bsnAPIfDBNoisePower.'
num_chan = 'AIRESPACE-WIRELESS-MIB::bsnAPIfPhyChannelNumber.'


def get_channel(chrange: str):
    """
    :param chrange: Base frequency: '0' - is 2.4 GHz, '1' - 5 GHz
    :return:
    """
    try:
        return query.get(oid=num_chan + args[2] + '.' + chrange).strip('ch\n')
    except:
        pass


def get_value(mib: str, apidx: str, chanrange: str):
    """
    :param mib:  First part of MIB
    :param apidx: AP Index
    :param chanrange: Base frequency: '0' - is 2.4 GHz, '1' - 5 GHz
    :return:
    """
    channel = get_channel(chanrange)
    if channel:
        try:
            return query.get(oid=mib + apidx + '.' + chanrange + '.' + channel)
        except:
            pass


if args[3] == 'InterferenceUtil24':
    print(get_value(interferencemib, args[2], '0'))
elif args[3] == 'InterferenceUtil5':
    print(get_value(interferencemib, args[2], '1'))
elif args[3] == 'NoisePower24':
    print(get_value(noisemib, args[2], '0'))
elif args[3] == 'NoisePower5':
    print(get_value(noisemib, args[2], '1'))
