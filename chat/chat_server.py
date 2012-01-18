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

Jon: This my server.  It only works with one client per ip.
Should I work on extending this to ip/port?

"""

import select
import socket
import sys
import time
import datetime

def send_data(host,port,data_to_send):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
    fail_count=0
    data=""
    
    try:
        s.connect((host,port))
        s.send(data_to_send) 
        data = s.recv(size)
        s.close()
        return "200"
    except:
        
        return "404"
    
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
print ''
print ''
print '   chat SERVER'
print '   running on %s' % my_name
print '   LISTENING on port %s' % listen_port 
print '   SENDING on port   %s' % send_port
print '______________________________________________________'
print''
print''

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
            if address[0] not in clients:
                clients.append (address[0])
                
                print "Added client: %s" % str(address[0])
            else:
                print "%s is an existing client" %  str(address[0])
            
            input.append(client)

        elif s == sys.stdin:
            # handle standard input
            junk = sys.stdin.readline()
            running = False
            print 'Input %s from stdin, exiting.' % junk.strip('\n')

        elif s: # A client sent something

            data = s.recv(size)
            
            if data:
                print '%s: sent <%s>' % (s.getpeername()[0], data.strip('\n'))
                s.send('200')

                #Spread the message to connected clients
                print "Messaging Clients:"
                for client in clients:
                    echo_client=my_name + ":" + s.getpeername()[0]+ ':'

                    #Skip the seneder
                    if s.getpeername()[0]!=client:
                        print "     Messaging %s on %i ..." % (client ,send_port),
                        #Try to send to the current client
                        if send_data(client,send_port,echo_client + data)=="200":
                            print "Success!!"
                        else:
                            print " FAILED."
                    else:
                        print "     Skipping sender %s on %i." % (client ,send_port)

                print
            else:
                s.close()
                input.remove(s)
                s.close()
