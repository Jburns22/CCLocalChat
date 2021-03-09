import socket
import select
import sys
import os
import ipScan
import time

IP_address = ipScan.IP
Port = ipScan.PORT

os.system('clear')
print(IP_address, Port, 'is open.')
time.sleep(.6)
print('Connection code received. Chatroom found.')

time.sleep(1)

name = input("Choose a username: ")
socket.setdefaulttimeout(.06)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((IP_address, Port))
client.send(name.encode('utf-8'))

while client.recv(1).decode('utf-8') == "0":
    name = input("Name taken. Choose another username: ")
    client.send(name.encode('utf-8'))
os.system('clear')

while True:
    sockets_list = [sys.stdin, client]
    read_sockets, write_socket, error_socket = select.select(sockets_list, [], [])
    for socks in read_sockets:
        if socks == client:
            try:
                message = socks.recv(2048).decode('utf-8')

            except:
                quit("Server disconnected. Exiting chatroom...")
            if message:

                w = message.split()

                if w[0] == "/xall":
                    client.close()
                    quit("Server disconnected. Exiting chatroom...")
                else:
                    print("\n"+message)
        else:

            message = sys.stdin.readline()
            client.send(message.encode('utf-8'))
            x = message.split()
            if x:
                if x[0] == "/x":
                    client.close()
                    quit("Exiting chatroom...")
                sys.stdout.flush()

