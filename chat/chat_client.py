"""
Assigment 2

In a new chat subdirectory, write a chat server based on
echo_server_select.  When any client sends a message, that message is
echoed to all clients, prefixed by the identification of the client
that sent the message (as well as the server that sent the message).

Test your chat server with two or more recho clients on localhost.
Will these servers work as intended with the recho client?  Why not?
If not, write a chat client, test your chat server with two or more
chat clients on local host, then run them on your VM.

Jon: This my client.  It only works with one client per ip.
Should I work on extending this to ip/port?
"""

import select
import socket
import sys
import time
import datetime

#Send data to a given host on a given port
def send_data(host,port,data_to_send):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
    s.connect((host,port)) 
    s.send(data_to_send) 

    data = s.recv(size)
    
    s.close()
    return data


host = 'localhost'#'block335046-zme.blueboxgrid.com'

#get the server name from the user
new_host=raw_input("Enter chat server")
if new_host !='' :
    host=new_host
port = 50003
listen_port=50004
size = 1024 
backlog = 5

#Set up a listener for messages from other users
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('',listen_port))


print
print
print '   chat CLIENT'

print '   SENDING on port   %s' % port
print '   LISTENING on port %s' % listen_port 
print '______________________________________________________'
print
print
server.listen(backlog)

timeout = 10 # seconds
input = [server,sys.stdin]

input_string=''

#Prompt the user to start chatting
print 'Enter the text to send(just hit enter to stop):'
while input_string!='\n':


    response=''
    #if we have input from the keyboard
    if input_string!='':
       #Send the input to the server
       response=send_data(host,port,input_string.strip('\n')
    
    input_string=''
    
    #Wait for input/messages from the server
    inputready,outputready,exceptready = select.select(input,[],[],timeout)

    #take a look at our input,if any
    for s in inputready:
        
        if s == server:
            # handle the server socket
            
            client, address = server.accept()
            input.append(client)

        elif s == sys.stdin:


            #If the user entered something, grab it to send to the server
            #If they just hit enter, we'll pop out of the loop
            input_string=sys.stdin.readline()
            
        elif s: #The server sent us a message
            data = s.recv(size)

            
            if data:
                #Echo the message back to the user
                print
                print  data.strip('\n')
                
                print
                
                
                s.send('200')
            else:
                s.close()
                
                input.remove(s)
                s.close()

print "Chat client exited"
print
print
