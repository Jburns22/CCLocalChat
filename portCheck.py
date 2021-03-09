import threading
import socket
import portCheck

# This program checks a specified port on a given IP.

found = 0
IP = 0
PORT = 0

socket.setdefaulttimeout(0.06)
print_lock = threading.Lock()


def portscan(t_IP,port):
    portCheck.found = 0
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((t_IP, port))
        with print_lock:
            s.send("0101".encode('utf-8'))
            try:
                message = s.recv(100).decode('utf-8')
            except: s.close()
            if message == "0101":
                portCheck.found = 1
                portCheck.IP = t_IP
                portCheck.PORT = port

            s.close()
    except:
        pass


