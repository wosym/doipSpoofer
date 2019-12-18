import threading

from comms import *



t1 = threading.Thread(target=tcp_server)
t2 = threading.Thread(target=udp_server)
t1.start()
t2.start()
t1.join()
t2.join()
