Client-Server Local Wifi Chatroom

This is a very basic terminal window chat room server with seperate files for clients and the host. The clients, by design, must all be in the same wifi range as each other and the host.

Chatroom Goals/Implementation

Implement a client-server architecture for a command prompt chat room. 

The reason we chose a client-server connection instead of peer to peer is because not every message is handled the same way, and not every message is meant for everyone. Some messages are meant to go to everyone, but others are meant to be delivered to a single recipient. Some command messages that clients can enter return information back to them, such as ‘/list’, which generates a list of all current users in the chatroom. Having a single point that receives all messages and interprets what should be done with them seemed appropriate.

Restrict connections to clients on the same wifi, as per the assignment instructions. 

To achieve this, a socket is opened at the start of the client program specifically to check the user’s IP and then the socket is closed. After this, the client script begins searching IPs within their IP range for a specific opened port. 

Implement a port scanner that will check if a given port is open across the client’s IP range. 

This was done by starting at the lowest IP within range, scanning for port 8081, and then adding 1 to the IP. IP addition was done by importing ipaddress. This process loops until the port is found open, or the maximum IP within range is reached. This implementation originally took a long time, but we introduced threading and it is now much, much faster. When an open port is found on an IP, the client tries to receive a specific code from the host. If it receives nothing, or if it receives a different code, it continues to search for the chatroom. This way, there are no false positives by way of an open port 8081 that is not the chatroom. 


Block any two users from using the same username. 

For obvious reasons, this would be a bad idea. Usernames need to be unique to the user, or they serve no purpose. When a user joins and enters a username, the server checks if a name already exists in its list of names. If it does, it requests a new, different username. 

Associate usernames with their corresponding connection. 

This is important because if a connection is lost, the corresponding username must be deleted from the list of active users. Otherwise a dropped connection would likely result in several user’s names being wrong, due to the change in the index of the connections when a connection is removed. 

Notify everyone in the chat when someone else enters/exits. 

In a chatroom, knowing both of these things are vital. You don’t want to share information with people you didn’t mean to, and you don’t want to end up talking to yourself by accident. This is seperate from the client’s ability to bring up a list of all active users because that requires prompting from the client, and user entrances/exits need to be announced immediately. A different solution that would solve both of these problems concurrently would be to always display the active users in chat somewhere on-screen.

Allow for sending messages to an individual and sending messages to everyone in chat. 

Sending messages to an individual is implemented by a whisper command ‘/w’ followed by a valid username. The server then finds the connection associated with that username and sends the private message. This is another reason why the server has to be able to associate connections and usernames. Sending a message to everyone except the sender is made possible through a loop that runs through a list of each connection. If the connection is not the one that sent the message, the message is delivered to that connection with the sender’s username attached to it. 


Allow users to see a list of all commands available to them. 

If a user isn’t aware of their capabilities in the chatroom, they have no way to use them! So, upon entrance to the chatroom a client receives a welcome message as well as a hint that if they type ‘/commands’ they will see a list of all the commands they can use, such as ‘/w’ to whisper, ‘/list’ to see all users, and ‘/x’ to exit. 


HOW TO USE

To use the chatroom, first run chatserver.py in a command window, and then run client.py in a different command window. This can be on the same computer or on a different computer, so long as they are on the same wifi. The other files (ipScan.py and portCheck.py) are called within the client.py script and therefore must be located in the same directory. 
