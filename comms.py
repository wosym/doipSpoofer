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
        data = binascii.hexlify(packet)
        print(f"Protocol version: {data[0:2]}")
        if(int(data[0:2]) == 2):
            print("Version is 2!")

        # Check for payload type
        if(int(data[4:8]) == 1):
                print("Payload Type: Vehicle Identification Request")
                reply = b'02fd000400000011aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
                reply = binascii.unhexlify(reply)
                sent = s.sendto(reply, source)
                print(reply)
                print(f"Sent {sent} bytes")

        elif(int(data[4:8]) == 8001):
                print("Payload Type: Diagnostic message")
                reply = b'02fd8002000000051a01e80100'
                reply = binascii.unhexlify(reply)
                sent = s.sendto(reply, source)
                print(reply)
                print(f"Sent {sent} bytes")

        print_doip_message(packet)
        process_doip_reply(packet)
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

                data = binascii.hexlify(packet)
                if(not data):
                    break   #connection close, break receive loop
                print("received DoIP message over TCP: %s" %data)
                if(int(data[0:2]) == 2):
                    print("Version is 2!")

                # Check for payload type
                if(int(data[4:8]) == 1):
                        print("Payload Type: Vehicle Identification Request")
                        reply = b'02fd000400000021aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa40100036f80140b60036f80140b6ff'
                        reply = binascii.unhexlify(reply)
                        sent = conn.sendall(reply)
                        print(reply)
                        print(f"Sent {sent} bytes")

                elif(int(data[4:8]) == 8001):
                        print("Payload Type: Diagnostic message")
                        reply = b'02fd8002000000051a01e80100'
                        reply = binascii.unhexlify(reply)
                        sent = conn.send(reply)
                        print(reply)
                        print(f"Sent {sent} bytes")


                print_doip_message(packet)
                print("====================================")
        finally:
            conn.close()
