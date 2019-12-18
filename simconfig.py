#class VehicleConfig():
VID = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'  #17 bytes
logical_address = 'bbbb'                    #2 bytes
EID = 'cccccccccccc'                        #6 bytes
GID = 'dddddddddddd'                        #6 bytes
further_action = 'ee'                                   #1 byte
sync_status = 'ff'                          #1 byte

def veh_ident_repl():
    return VID+logical_address+EID+GID+further_action+sync_status
