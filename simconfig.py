'''
'
' Simulator config
'
' @brief: configuration file for the DoIP spoofer
' @author   Wouter Symons <wsymons@nalys-group.com>
'''
#class VehicleConfig():
VID = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'  #17 bytes
logical_address = 'bbbb'                    #2 bytes
EID = 'cccccccccccc'                        #6 bytes
GID = 'dddddddddddd'                        #6 bytes
further_action = 'ee'                                   #1 byte
sync_status = 'ff'                          #1 byte
diagnostics_data = {
    b'\xf1\xaa' : b'\x4a\x32\x38\x35\x20',
    b'\xff\xff' : b'\x11\x33\x22\x45\x98',
    b'\x10\x12' : b'\x45\x14\x87\xfe\x2c',
    b'\xee\xbb' : b'\x12\x65\xde\xad\x32',
    #TODO: add more sample data
}

def veh_ident_repl():
    return VID+logical_address+EID+GID+further_action+sync_status
