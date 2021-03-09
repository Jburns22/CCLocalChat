import socket
from _thread import *
import chatserver
import os

# This program receives incoming messages from all clients and interprets
# what it should do with a given message, be it broadcasting it to everyone else,
# sending a given message to an individual recipient, removing the sender from the chatroom, or
# sending requested information back to the sender-client.

os.system('clear')
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
IP_address = (s.getsockname()[0])
s.close()

# This socket is just to identify the IP of the host, and is immediately closed after.

Port = 8081

print("------------------------------")
print("Server IP: ", IP_address, "      |")
print("Server Port: ", Port, "           |")
server.bind((IP_address, Port))

# binds the server to an entered IP address and at the specified port number.

server.listen(100)

# listens for 100 active connections. This number can be increased as per convenience

print("Chatroom initialized.         |")
print("(Control+C to close server)   |")
print("------------------------------\n")
print("Waiting for clients...\n")

list_of_clients = []
name = []
count = 0


def clientThread(connection, username):
    connection.send(("                          Welcome to the chatroom " + username + "!\n"
    "--------------------------------------------------------------------------------\n(Type /commands "
    "for a list "
    "of user commands)\n").encode('utf-8'))
    connection.send("\nCurrent Users:\n".encode('utf-8'))

    for x in name:
        message = x
        connection.send(("<" + message + ">\n").encode('utf-8'))

    joined = "<" + username + "> joined the chat.\n"
    broadcast(joined, connection)

    while True:

        try:
            message = connection.recv(2048).decode('utf-8')

            if message:
                w = message.split()

                if w[0] == '/x':
                    remove(connection, username)

                elif w[0] == "/w":
                    whisper(message, username)
                elif w[0] == "/me":
                    connection.send(("Your username is: <" + username + ">").encode('utf-8'))
                elif w[0] == "/list":
                    connection.send("\nCurrent Users:\n".encode('utf-8'))
                    for x in name:
                        message = x
                        connection.send(("<" + message + ">\n").encode('utf-8'))
                elif w[0] == "/commands":
                    commandList = '/list: shows all users currently in chat.\n/w (followed by a valid username): ' \
                                  'whispers a message to the specified user.\n/x: exits chat\n/me: displays your ' \
                                  'username\n '
                    connection.send(commandList.encode('utf-8'))
                else:
                    print("<" + username + "> " + message)
                    message_to_send = "<" + username + "> " + message
                    broadcast(message_to_send, connection)

        except:
            continue


def ender():
    print("losing server...")
    broadcast("/xall", '255.255.255.255')


def broadcast(message, connection):
    index = 0
    for clients in list_of_clients:
        if clients != connection:
            index = index + 1
            try:
                clients.send(message.encode('utf-8'))
            except:
                clients.close()
                remove(clients, name[index])


def remove(connection, username):
    if connection in list_of_clients:
        broadcast(username + " exited chat.\n", connection)
        list_of_clients.remove(connection)
        name.remove(username)
        chatserver.count = chatserver.count - 1
        print(username + " exited chat.")


def whisper(message, sender):
    split = message.split(' ', 2)
    index = 0
    for username in name:
        if username == split[1]:
            message_to_send = "[Whisper from <" + sender + ">] " + split[2]
            list_of_clients[index].send(message_to_send.encode('utf-8'))
            break
        index = index + 1


while True:
    try:
        conn, addr = server.accept()

    except:
        quit(ender())

    # maintains a list of clients for ease of broadcasting a message to all available people in the chatroom
    # Prints the address and username of the person who just connected

    code = conn.recv(2048).decode('utf-8')
    if code == '0101':
        conn.send("0101".encode('utf-8'))

    else:
        nome = code

        if nome:
            while nome in name:
                conn.send("0".encode('utf-8'))
                nome = conn.recv(2048).decode('utf-8')
            conn.send("1".encode('utf-8'))
            list_of_clients.append(conn)
            name.append(nome)
            start_new_thread(clientThread, (conn, name[count]))

            if count == 0:
                os.system('clear')
                print("------------------------------")
                print("Server IP: ", IP_address, "      |")
                print("Server Port: ", Port, "           |")
                print("Chatroom initialized.         |")
                print("(Control+C to close server)   |")
                print("------------------------------\n")
            print(addr[0], "connected as", name[count])
            count = count + 1
        else:
            conn.close()
