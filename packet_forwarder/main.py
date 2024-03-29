#!/usr/bin/env python3

import logging
import signal
import sys
import re
import libyang
import scapy.layers.l2
import sysrepo
from scapy.layers.inet import *
from scapy.layers.l2 import *
from scapy.all import *
import time
import threading


INPUT_NIC = 'eth1'
OUT_NIC1 = 'eth2'
OUT_NIC2 = 'eth3'

routeList = []
sysrepoSess = ''


class Route:

    def __init__(self, protocol, in_iface, out_iface):
        self.protocol = protocol
        self.in_iface = in_iface
        self.out_iface = out_iface


def pkt_callback_LTR1(pkt):
    global routeList

    if pkt.haslayer(ARP):
        return True

    for route in routeList:
        if route.out_iface == OUT_NIC1:
            for allowedProto in route.protocol:
                if pkt.haslayer(allowedProto):
                    return True
    # pkt.show()
    return False



def pkt_callback_LTR2(pkt):
    global routeList
    if pkt.haslayer(ARP):
        return True
    for route in routeList:
        if route.out_iface == OUT_NIC2:
            for allowedProto in route.protocol:
                if pkt.haslayer(allowedProto):
                    return True
    # pkt.show()
    return False


def pkt_callback_RTL1(pkt):
    return True

def pkt_callback_RTL2(pkt):
    return True


def enableConnectionL_R1():
    bridge_and_sniff(if1=INPUT_NIC, if2=OUT_NIC1,
                     xfrm12=pkt_callback_LTR1, xfrm21=pkt_callback_RTL1,
                     count=0, store=0)

def enableConnectionL_R2():
    bridge_and_sniff(if1=INPUT_NIC, if2=OUT_NIC2,
                     xfrm12=pkt_callback_LTR2, xfrm21=pkt_callback_RTL2,
                     count=0, store=0)


def main():
    logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s] application: %(message)s")
    sysrepo.configure_logging(py_logging=True)

    enableConnectionL_R1_Thread = threading.Thread(target=enableConnectionL_R1,args=())
    enableConnectionL_R1_Thread.start()

    enableConnectionL_R2_Thread = threading.Thread(target=enableConnectionL_R2, args=())
    enableConnectionL_R2_Thread.start()

    try:
        with sysrepo.SysrepoConnection() as conn:
            with conn.start_session() as sess:
                global sysrepoSess
                global routeList

                logging.info("subscribing to module sfc-route")
                sess.subscribe_module_change("sfc-route", None, sfc_route_change_callback)
                sysrepoSess = sess
                # Reading the module data in case when the module is populated before running this app. since the datastore
                # is populated with data already the "subscribe_module_change" does not show any data, so we need to read the initial dat (if any)
                #using the below function!
                data = sess.get_data("/sfc-route:sfc_routes")
                ## if mot empty-> {'sfc_routes': {'route': [{'protocol': 'tcp', 'in_iface': 'eth0', 'out_iface': 'eth2'}, {'protocol': 'udp', 'in_iface': 'eth0', 'out_iface': 'br0'}]}}
                ## if empty-> {}
                if data:
                    print(data)
                    for route in data['sfc_routes']['route']:
                        allowedProto = []
                        if len(str(route['protocol']).split(",")) > 1:
                            for proto in str(route['protocol']).split(","):
                                if proto == "tcp":
                                    allowedProto.append(TCP)
                                elif proto == "icmp":
                                    allowedProto.append(ICMP)
                                elif proto == "udp":
                                    allowedProto.append(UDP)
                        else:
                            if route['protocol'] ==  "tcp":
                                allowedProto.append(TCP)
                            elif route['protocol'] ==  "icmp":
                                allowedProto.append(ICMP)
                            elif route['protocol'] ==  "udp":
                                allowedProto.append(UDP)

                        routeList.append(Route(allowedProto, route['in_iface'], route['out_iface']))

                signal.sigwait({signal.SIGINT, signal.SIGTERM})
                enableConnectionL_R1_Thread.join()
                enableConnectionL_R2_Thread.join()
        return 0
    except sysrepo.SysrepoError as e:
        logging.error("%s", e)
        return 1


def sfc_route_change_callback(event, req_id, changes, private_data):
    global sysrepoSess
    global routeList
    routeList= []
    data = sysrepoSess.get_data("/sfc-route:sfc_routes")
    if data:
        for route in data['sfc_routes']['route']:
            allowedProto = []
            if len(str(route['protocol']).split(",")) > 1:
                for proto in str(route['protocol']).split(","):
                    if proto == "tcp":
                        allowedProto.append(TCP)
                    elif proto == "icmp":
                        allowedProto.append(ICMP)
                    elif proto == "udp":
                        allowedProto.append(UDP)
            else:
                if route['protocol'] == "tcp":
                    allowedProto.append(TCP)
                elif route['protocol'] == "icmp":
                    allowedProto.append(ICMP)
                elif route['protocol'] == "udp":
                    allowedProto.append(UDP)
            routeList.append(Route(allowedProto, route['in_iface'], route['out_iface']))

    # for route in routeList:
    #     print("$$$$$$$$$$$$$$$$$$$$$$$$")
    #     for pr in route.protocol:
    #         print(pr.name)
    #     print(" | " + route.in_iface + " | " + route.out_iface)
    #     print("$$$$$$$$$$$$$$$$$$$$$$$$")

if __name__ == "__main__":
    sys.exit(main())





