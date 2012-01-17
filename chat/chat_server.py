"""
Based on Daniel Zappala's http://ilab.cs.byu.edu/python/code/echoserver-select.py
Add print statements to show what's going on.
Use SO_REUSEADDR to avoid 'Address already in use' errors
Add timeout
make style similar to our recho_clien

An echo server that uses select to handle multiple clients at a time.
Entering any line of input at the terminal will exit the server.
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
    while fail_count<10:
        try:
            s.connect((host,port))
            s.send(data_to_send) 
            data = s.recv(size)
            
            return data
            s.close()
            
        except:
            fail_count+=1
            print"          Fail %i" % fail_count
            time.sleep(1)
            
        
    print "send failed"
    


    
host = ''
port = 50003 # different port than other samples, all can run on same server
send_port=50004
if len(sys.argv) > 1:
    port = int(sys.argv[1])

backlog = 5
size = 1024

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Release listener socket immediately when program exits, 
# avoid socket.error: [Errno 48] Address already in use
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((host,port))

#print 'echo_server listening on port %s, to exit type return ' % port


print
print
print '   chat SERVER'
print '   LISTENING on port %s' % port 
print '   SENDING on port   %s' % send_port
print '______________________________________________________'
print
print

server.listen(backlog)

timeout = 10 # seconds
input = [server,sys.stdin]
running = True
clients=[]

while running:
    
    inputready,outputready,exceptready = select.select(input,[],[],timeout)
    
    # timeout
    


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

        elif s: # client socket


            data = s.recv(size)
            
            if data:
                print '%s: sent <%s>' % (s.getpeername()[0], data.strip('\n'))
                s.send('200')
                print "Messaging Clients:"
                for client in clients:
                    echo_client=s.getpeername()[0]+ ' said:'
                    print "     Messaging %s on %i ..." % (client ,send_port),
                    if s.getpeername()[0]==client:
                        echo_client="YOU said:"
                    if send_data(client,send_port,echo_client + data)=="200":
                        print "Success!!"
                    else:
                        print "FAILED"

                print
            else:
                s.close()
                input.remove(s)
                s.close()
