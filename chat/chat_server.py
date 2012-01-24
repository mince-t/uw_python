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


"""

import select
import socket
import sys
import time
import datetime

    
host = ''
listen_port = 50003

#Get my fqdn
my_name=socket.getfqdn(socket.gethostname())

#Port used to spread messages to clients
send_port=50004
if len(sys.argv) > 1:
    listen_port = int(sys.argv[1])

backlog = 5
size = 1024

#tool up to listen for inbound chat messages
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((host,listen_port))

#let the user know what's going on
print '\n'*10
print '____________________________________________'
print '   CHAT SERVER'
print '   RUNNING ON %s' % my_name
print '   LISTENING LISTENING ON %s' % listen_port 

print '____________________________________________'
print '\n'*10
#start listening
server.listen(backlog)

timeout = 10 
input = [server,sys.stdin]
running = True

#our list of connected clients
clients=[]

while running:
    
    inputready,outputready,exceptready = select.select(input,[],[],timeout)
    
    for s in inputready:

        if s == server:
            # handle the server socket
            
            client, address = server.accept()
            print
            print 'accepted connection from', address
            
            
            input.append(client)

        elif s == sys.stdin:
            # handle standard input
            junk = sys.stdin.readline()
            running = False
            print 'Input %s from stdin, exiting.' % junk.strip('\n')

        elif s: # A client sent something

            data = s.recv(size)

                
            if data:
                
                
                print "%s on port %s says '%s'" % (s.getpeername()[0],s.getpeername()[1], data.strip('\n'))

                #Spread the message to connected clients
                print "Messaging Clients:"
                for client_sock in input:
                    
                    if client_sock != server and client_sock!=sys.stdin:
                        
                        
                        response="%s>%s:%s>%s" % (my_name,s.getpeername()[0],s.getpeername()[1],data.strip('/n'))
                        print '%15s on port %s' % (client_sock.getpeername())
                        client_sock.send(response)
            else:
                print "a client has exited"
                
                s.close()
                input.remove(s)
                s.close()
