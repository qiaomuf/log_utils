#!/usr/bin/env python

"""
10:51:06.108705 IP m1-www-fbs101.m1.baidu.com.60806 > jx-ps-jx-0-43.jx.baidu.com.11745: P 1:980(979) ack 1 win 46 <nop,nop,timestamp 751062567 4210957872>
10:51:06.108709 IP jx-ps-jx-0-43.jx.baidu.com.11745 > m1-www-fbs101.m1.baidu.com.60806: . ack 980 win 61 <nop,nop,timestamp 4210957873 751062567>
10:51:06.132184 IP jx-ps-jx-0-43.jx.baidu.com.11745 > m1-www-fbs101.m1.baidu.com.60806: P 1:453(452) ack 980 win 61 <nop,nop,timestamp 4210957896 751062567>
10:51:06.133170 IP m1-www-fbs101.m1.baidu.com.60806 > jx-ps-jx-0-43.jx.baidu.com.11745: . ack 453 win 54 <nop,nop,timestamp 751062592 4210957896>
"""
"""
Network Packets:
bc request bs
bs ack bc
bs response bc
bc ack bs

So we only care about bc to bs
"""

import sys
from optparse import OptionParser

def inactive_handler(conn):
    diff = conn.end_dt - conn.start_dt
    print "%s:%s %s:%s %d"%(conn.from_host, conn.from_port, conn.to_host, conn.to_port, diff.microseconds)
    #for packet in conn.packets:
    #    print packet

class BcConnection:
    def __init__(self, from_host, from_port, to_host, to_port):
        self.from_host = from_host
        self.from_port = from_port
        self.to_host = to_host
        self.to_port = to_port

        self.start_dt = None
        self.end_dt = None

        self.active = False

        self.inactive_handler = inactive_handler
        self.packets = []

    def add_event(self, time, packet, from_host, from_port, to_host, to_port):
        #print packet
        from datetime import datetime
        self.packets.append((from_host, from_port, to_host, to_port, time, packet))
        if self.is_bc_request(packet, from_host, from_port, to_host, to_port):
            #self.start_dt = datetime.strptime(time, '%H:%M:%S.%f')
            today = datetime.today()
            self.start_dt = datetime(today.year, today.month, today. day, hour=int(time[0:2]), minute=int(time[3:5]), second=int(time[6:8]), microsecond=int(time[9:]))
            self.active = True
            return True
        elif self.active and self.is_fin(packet, from_host, from_port, to_host, to_port):
            self.active = False
            return False
        elif self.active and self.is_bs_response(packet, from_host, from_port, to_host, to_port):
        #elif self.active and self.is_bc_ack(packet, from_host, from_port, to_host, to_port):
            #self.end_dt = datetime.strptime(time, '%H:%M:%S.%f')
            today = datetime.today()
            self.end_dt = datetime(today.year, today.month, today. day, hour=int(time[0:2]), minute=int(time[3:5]), second=int(time[6:8]), microsecond=int(time[9:]))
            diff = self.end_dt - self.start_dt
            self.inactive_handler(self)
            self.active = False
            return True
        else:
            return False

    def bc_to_bs(self, from_host, from_port, to_host, to_port):
        return from_host == self.from_host and from_port == self.from_port and to_host == self.to_host and to_port == self.to_port

    def bs_to_bc(self, from_host, from_port, to_host, to_port):
        return from_host == self.to_host and from_port == self.to_port and to_host == self.from_host and to_port == self.from_port

    def is_bc_request(self, packet, from_host, from_port, to_host, to_port):
        # different tcpdump version
        return self.bc_to_bs(from_host, from_port, to_host, to_port) and (packet.startswith('P ') or packet.startswith('Flags [P.], seq'))

    def is_bc_ack(self, packet, from_host, from_port, to_host, to_port):
        # different tcpdump version
        #return packet.find('ack') != 0 or packet.startswith('Flags [.], ack')
        return self.bc_to_bs(from_host, from_port, to_host, to_port) and (packet.startswith('. ack') != 0 or packet.startswith('Flags [.], ack'))

    def is_bs_response(self, packet, from_host, from_port, to_host, to_port):
        return self.bs_to_bc(from_host, from_port, to_host, to_port) and (packet.startswith('P ') or packet.startswith('Flags [P.], seq'))

    def is_fin(self, packet, from_host, from_port, to_host, to_port):
        return packet.startswith('Flags [F.], seq')

    def set_inactive_handler(self, func):
        self.inactive_handler = func

def get_host_port(host_port):
    split_pos = host_port.rfind('.')
    return host_port[:split_pos], host_port[split_pos + 1:]

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-b', '--bs', help='bs host', dest='bs_host')
    parser.add_option('-p', '--port', help='comma separated bs ports', dest='bs_ports')
    (options, args) = parser.parse_args()

    BcConnections = {}
    bs_ports = options.bs_ports.split(',')
    for line in sys.stdin:
        values = line.strip().split()
        if not values:
            continue
        time = values[0]
        from_host, from_port = get_host_port(values[2])
        to_host, to_port= get_host_port(values[4][:-1])
        packet = ' '.join(values[5:])
        #print to_host, options.bs_host, to_port, bs_ports
        #print to_port
        if to_host == options.bs_host and to_port in bs_ports:
            conn_id = from_host + from_port + to_host + to_port
            if conn_id not in BcConnections:
                BcConnections[conn_id] = BcConnection(from_host, from_port, to_host, to_port)
            conn = BcConnections[conn_id]
        else:
            conn_id = to_host + to_port + from_host + from_port
            if conn_id in BcConnections:
                conn = BcConnections[conn_id]
            else:
                conn = None

        if conn and not conn.add_event(time, packet, from_host, from_port, to_host, to_port):
            pass
