import ipaddress
from portCheck import *
import os

# This program loops the portCheck script on every IP within range of the
# user's connection until the designated port is found open or the range is
# exhausted.

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip = (s.getsockname()[0])
s.close()

# This socket is just to identify the IP of the client, and is immediately closed after.

start = list(ip.split("."))
start[3] = '0'
start[2] = '0'

end = list(ip.split("."))
end[3] = '255'
end[2] = '255'

startstring = start[0] + "." + start[1] + "." + start[2] + "." + start[3]
startip = ipaddress.IPv4Address(startstring)

endstring = end[0] + "." + end[1] + "." + end[2] + "." + end[3]
endip = ipaddress.IPv4Address(endstring)

tempip = startip


def loop(tempip, endip):
    port = 8081
    while portCheck.found == 0 and tempip <= endip:
        target = str(tempip)
        portscan(target, port)
        tempip = tempip + 50


def loopPrint(tempip, endip):
    print_counter = 0
    port = 8081
    while portCheck.found == 0 and tempip <= endip:
        target = str(tempip)
        portscan(target, port)
        tempip = tempip + 50
        if print_counter <= 5:
            os.system('clear')
            print("Scanning.")
            print_counter = print_counter + 1
        elif print_counter <= 10:
            os.system('clear')
            print("Scanning..")
            print_counter = print_counter + 1
        elif print_counter <= 15:
            os.system('clear')
            print("Scanning...")
            print_counter = print_counter + 1
        elif print_counter <= 20:
            os.system('clear')
            print("Scanning...")
            print_counter = 0


def Threader():
    threads = []
    thread_count = 0
    for n in range(50):
        t = threading.Thread(target=loop, args=(tempip + thread_count, endip))
        t.start()
        threads.append(t)
        thread_count = thread_count + 1


Threader()
loopPrint(startip, endip)

IP = portCheck.IP
PORT = portCheck.PORT
