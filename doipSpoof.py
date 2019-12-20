'''
'
' DoIP Spoofer
'
' @brief: Tool used to simulate a DoIP diagnostics session in a car
' @author   Wouter Symons <wsymons@nalys-group.com>
'''
import threading

from comms import *



t1 = threading.Thread(target=tcp_server)
t2 = threading.Thread(target=udp_server)
t1.start()
t2.start()
t1.join()
t2.join()
