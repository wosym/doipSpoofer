'''
'
' DoIP Spoofer: communications
'
' @brief: Communication handling functions for the DoIP spoofer
' @author   Wouter Symons <wsymons@nalys-group.com>
'''
import socket
import binascii
import time
import sys
from struct import *

from doip_util import *

def udp_server():
    try:
        s= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except (socket.error):
        print("Error creating socket: " )
        sys.exit()

    server_adress = ('192.168.0.11', 13400) #TODO: make settable through arguments
    print("Starting UDP server on %s port %s" % server_adress)
    s.bind(server_adress)
    while True:
        packet, source = s.recvfrom(4096)

        print("Incoming DoIP message over UDP from ip: %s srcport: %s" % (source[0], source[1]))
        print_doip_message(packet)
        reply = process_doip_reply(packet)
        print("Replying with:")
        print_doip_message(reply)
        sent = s.sendto(reply, source)
        print(f"Sent {sent} bytes")
        print("====================================")

def tcp_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('192.168.0.11', 13400)    #TODO: make settable through arguments
    print("starting TCP server on %s port %s" % server_address)
    sock.bind(server_address)

    sock.listen(1)

    while True:
        conn, client_address = sock.accept()

        try:
            while True:
                packet = conn.recv(16)

                if(not packet):
                    break
                print_doip_message(packet)
                reply = process_doip_reply(packet)
                if isinstance(reply, list):
                    for r in reply:
                        print("Replying with:")
                        print_doip_message(r)
                        sent = conn.send(r)
                        print(f"Sent {sent} bytes")
                else:
                    print("Replying with:")
                    print_doip_message(reply)
                    sent = conn.send(reply)
                    print(f"Sent {sent} bytes")
                print("====================================")
        finally:
            conn.close()
