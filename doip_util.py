from doip import *
from scapy.all import *
from scapy.contrib.automotive.uds import *
from simconfig import VehicleConfig


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

def create_doip_reply(ta='00', sa='00', msg_type=0x0000, uds_service="", doip_pl=""):
    uds_pl = ""
    pl_len = 0
    if uds_service:
        uds_pl = UDS(service=uds_service)
        print("uds_pl:")
        print(uds_pl)

    pl_len = len(doip_pl) + len(uds_pl)

    if(msg_type != 0x0004): #TODO: there's probably more messages whithout SA/TA
        pl_len += 4
    doip = DoIPRawPacket(payload_type=msg_type, payload_length=pl_len,payload_content=bytearray.fromhex(ta+sa+doip_pl))

    return doip/uds_pl

def process_doip_reply(msg):
    msg = DoIPRawPacket(msg)
    if(not (msg.protocol_version == 0x02 and msg.inverse_version == 0xFD)):
        return None

    print("Incoming: " + payload_types[msg.payload_type])
    if msg.payload_type == 0x0000:
        print("TODO: no response implemented for this message yet")
    elif msg.payload_type == 0x0001:
        rep = create_doip_reply(msg_type=0x0004, doip_pl=VehicleConfig.VID)
        print("reply: ")
        print(rep)
    elif msg.payload_type == 0x0002:
        print("TODO: no response implemented for this message yet")
    elif msg.payload_type == 0x0003:
        print("TODO: no response implemented for this message yet")
    elif msg.payload_type == 0x0004:
        print("TODO: no response implemented for this message yet")
    else:
        print("unknown DoIP message type")

