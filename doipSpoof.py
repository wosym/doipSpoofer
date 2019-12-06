import sys
import socket
from struct import *
import binascii


try:
    s= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except (socket.error):
    print("Error creating socket: " )
    sys.exit()

#server_adress = ('169.254.161.102', 13400)
server_adress = ('192.168.0.20', 13400)
print("Starting capture on %s port %s" % server_adress)
s.bind(server_adress)
while True:
    packet, source = s.recvfrom(4096)
    #print(packet)
    #print(len(packet))

    print("Incoming message from ip: %s srcport: %s" % (source[0], source[1]))
    data = binascii.hexlify(packet)
    print(data)
    print(f"Protocol version: {data[0:2]}")
    if(int(data[0:2]) == 2):
        print("Version is 2!")

    # Check for payload type
    if(int(data[4:8]) == 1):
            print("Payload Type: Vehicle Identification Request")
            #reply = b'02fd000400000004aaaaaaaaaaaaaaaaaa4010ccccccddddddef'
            reply = b'02fd000400000021aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa40100036f80140b60036f80140b6ff'
            reply = binascii.unhexlify(reply)
            sent = s.sendto(reply, source)
            print(reply)
            print(f"Sent {sent} bytes")

    elif(int(data[4:8]) == 8001):
            reply = b'02fd8002000000051a01e80100'
            reply = binascii.unhexlify(reply)
            sent = s.sendto(reply, source)
            print("Payload Type: Diagnostic message")


    print("====================================")



