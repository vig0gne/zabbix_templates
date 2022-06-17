#!/usr/bin/python3
"""
:param arg[1] - Controller Address
:param arg[2] - AP Index
:param arg[3] - Case
:param arg[4] - SNMP Community
"""

from snmp_cmds import *
import sys


args = sys.argv
query = Session(ipaddress=args[1], read_community=args[4])
interferencemib = 'AIRESPACE-WIRELESS-MIB::bsnAPIfInterferenceUtilization.'
noisemib = 'AIRESPACE-WIRELESS-MIB::bsnAPIfDBNoisePower.'


def get_channel(chrange: str):
    """
    :param chrange: Base frequency: '0' - is 2.4 GHz, '1' - 5 GHz
    :return:
    """
    return query.get(oid='AIRESPACE-WIRELESS-MIB::bsnAPIfPhyChannelNumber.' + args[2] + '.' + chrange).strip('ch\n')


def get_value(mib: str, apidx: str, chanrange: str):
    """
    :param mib:  First part of MIB
    :param apidx: AP Index
    :param chanrange: Base frequency: '0' - is 2.4 GHz, '1' - 5 GHz
    :return:
    """
    return query.get(oid=mib + apidx + '.' + chanrange + '.' + get_channel(chanrange))


action = {'InterferenceUtil24': get_value(interferencemib, args[2], '0'),
          'InterferenceUtil5': get_value(interferencemib, args[2], '1'),
          'NoisePower24': get_value(noisemib, args[2], '0'),
          'NoisePower5': get_value(noisemib, args[2], '1')}

if args[3] in action:
    print(action.get(args[3]))
