from doip import *
from scapy.all import *
from scapy.contrib.automotive.uds import *


def print_doip_message(msg):
    doip = DoIPRawPacket(msg)
    if(doip.protocol_version == 0x02 and doip.inverse_version == 0xFD):
        doip.show()
        if(doip.payload_length >=4):
            print(f"SA: {doip.payload_content[0:2]}, TA: {doip.payload_content[2:4]}")
        if(doip.payload_length >=5):
            uds_payload = DoIPRawPacket(msg).payload_content[4:]
            UDS(uds_payload).show()
    else:
        print("Message is not of DoIP type")

    return

def create_doip_reply(ta='00', sa='00'):
    uds = UDS(service="TesterPresent")/UDS()
    doip = DoIPRawPacket(payload_type=0x8001, payload_length=4 + len(uds),payload_content=bytearray.fromhex(ta+sa))

    return doip/uds
