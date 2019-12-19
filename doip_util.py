from doip import *
from scapy.all import *
from scapy.contrib.automotive.uds import *
import simconfig
from binascii import unhexlify, hexlify
from time import sleep

def print_doip_message(msg):
    doip = DoIPRawPacket(msg)
    if(doip.protocol_version == 0x02 and doip.inverse_version == 0xFD):
        doip.show()
        if(doip.payload_length >=4):
            print(f"SA: {doip.payload_content[0:2]}, TA: {doip.payload_content[2:4]}")
        if(doip.payload_type >=4000):
            uds_payload = DoIPRawPacket(msg).payload_content[4:]
            UDS(uds_payload).show()
    else:
        print("Message is not of DoIP type")
    return

def create_doip_reply(ta='', sa='', msg_type=0x0000, doip_pl=b'', uds_service="", uds_data=None):
    uds_pl = ""
    pl_len = 0
    if uds_service:
        uds_pl = UDS(service=uds_service)/Raw(uds_data)
        pl_len += len(uds_pl)

    pl_len += len(doip_pl)

    if(not(sa == '' and ta== '')):
        pl_len += 4

    doip = DoIPRawPacket(payload_type=msg_type, payload_length=pl_len,payload_content=bytearray.fromhex(sa+ta)+doip_pl)

    return doip/uds_pl

def process_doip_reply(msg):
    msg = DoIPRawPacket(msg)
    rep = None
    if(not (msg.protocol_version == 0x02 and msg.inverse_version == 0xFD)):
        return None

    try:
        dmt = payload_types[msg.payload_type]
        print("DoIP message type: " + dmt)
    except:
        print("DoIP message type not found")

    #TODO:  change all 0x___ with name
    if msg.payload_type == 0x0000:
        print("TODO: no response implemented for this message yet")
        rep = bytes(create_doip_reply(msg_type=0x0000))
    elif dmt == "vehicle identification request message":
        rep = bytes(create_doip_reply(msg_type=0x0004, doip_pl=bytearray.fromhex(simconfig.veh_ident_repl())))
    elif msg.payload_type == 0x0002:
        print("TODO: no response implemented for this message yet")
        rep = bytes(create_doip_reply(msg_type=0x0000))
    elif msg.payload_type == 0x0003:
        print("TODO: no response implemented for this message yet")
        rep = bytes(create_doip_reply(msg_type=0x0000))
    elif msg.payload_type == 0x0004:
        print("TODO: no response implemented for this message yet")
        rep = bytes(create_doip_reply(msg_type=0x0000))
    elif dmt == "diagnostic message":
        did = UDS(msg.payload_content[4:]).service
        try:
            sv = UDS.services[did]
            print("UDS service: " + sv )
        except:
            sv = None
            print("UDS service not found")
        if sv == "TesterPresent":
            # --> send diagnostic nack, nack code: 02
            rep = bytes(create_doip_reply(msg_type=0x8003, sa=str(msg.payload_content[2:4].hex()), ta=str(msg.payload_content[0:2].hex()), doip_pl=b'\x02'))    #TODO: tester present positive response
        elif sv == "ReadDataByIdentifier":
            #send ack, doip_code: 01
            rep = [0,0]    #in this case, there will be multiple replies
            rep[0] = bytes(create_doip_reply(msg_type=0x8002, sa=str(msg.payload_content[2:4].hex()), ta=str(msg.payload_content[0:2].hex()), doip_pl=b'\x01'))
            sleep(0.5)
            #send actual data
            try:
                uds_reply = msg.payload_content[5:] + simconfig.diagnostics_data[msg.payload_content[5:]]
                rep[1] = bytes(create_doip_reply(msg_type=0x8001, sa=str(msg.payload_content[2:4].hex()), ta=str(msg.payload_content[0:2].hex()), uds_service="ReadDataByIdentifierPositiveResponse" , uds_data=uds_reply))
            except KeyError:    #ECU ID not in LUT
                print("ECU ID not in LUT!")
                rep[1] = bytes(create_doip_reply(msg_type=0x8001, sa=str(msg.payload_content[2:4].hex()), ta=str(msg.payload_content[0:2].hex()), uds_service="NegativeResponse"))  #TODO: malformed?
        else:
            print("Diagnostic msg not implemented yet")
            rep = bytes(create_doip_reply(msg_type=0x0000))
    else:
        print("unknown DoIP message type")
        rep = bytes(create_doip_reply(msg_type=0x0000))

    if not rep:
        rep = bytes(create_doip_reply(msg_type=0x0000))


    return rep
