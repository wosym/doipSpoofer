import binascii
import socket
from struct import *
import sys
import threading
import time
from scapy.all import *
from doip import *
from scapy.contrib.automotive.uds import *


def decode_doip_message(msg):
    try:
        DoIPRawPacket(msg).show()
        uds_payload = DoIPRawPacket(msg).payload_content[4:]
        print(uds_payload)
        UDS(uds_payload).show()
    except TypeError:
        print("typeError")
    return

def create_doip_reply(ta='00', sa='00'):
    uds = UDS(service="TesterPresent")/UDS()
    doip = DoIPRawPacket(payload_type=0x8001, payload_length=4 + len(uds),payload_content=bytearray.fromhex(ta+sa))

    #My guess is that we don't need these when we use the sockets. We could ofcourse use scapy send, but then we'd have to convert the source addresses, which makes it unnecesarrily complicated.
    #udp = UDP(dport=13400, sport=13400)
    #ip = IP(dst="127.0.0.1")

    #r = send(ip/udp/doip/uds)

    return doip/uds


def udp_server():
    try:
        s= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except (socket.error):
        print("Error creating socket: " )
        sys.exit()

#server_adress = ('169.254.161.102', 13400)
    server_adress = ('192.168.0.11', 13400)
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
                #reply = b'02fd000400000004aaaaaaaaaaaaaaaaaa4010ccccccddddddef'
                #reply = b'02fd000400000021aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa40100036f80140b60036f80140b6ff'
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

        decode_doip_message(packet)
        print("====================================")

def tcp_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('192.168.0.11', 13400)
    print("starting TCP server on %s port %s" % server_address)
    sock.bind(server_address)

    sock.listen(1)

    while True:
        conn, client_address = sock.accept()

        try:
        #    print("connection from %s - %s " % client_address)

            while True:
                packet = conn.recv(16)

                data = binascii.hexlify(packet)
                if(not data):
        #            print("Connection closed")
                    break   #connection close, break receive loop
                print("received DoIP message over TCP: %s" %data)
                if(int(data[0:2]) == 2):
                    print("Version is 2!")

                # Check for payload type
                if(int(data[4:8]) == 1):
                        print("Payload Type: Vehicle Identification Request")
                        #reply = b'02fd000400000004aaaaaaaaaaaaaaaaaa4010ccccccddddddef'
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


                decode_doip_message(packet)
                print("====================================")
        finally:
            conn.close()


#tcp_server()
t1 = threading.Thread(target=tcp_server)
t2 = threading.Thread(target=udp_server)
t1.start()
t2.start()
t1.join()
t2.join()
