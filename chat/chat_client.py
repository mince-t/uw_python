"""
echo client, usage:

 python echo_client.py <host> <port>

Both host and port are optional, defaults: localhost 50000
host must be present if you want to provide port
"""

import select
import socket
import sys
import time
import datetime
def send_data(host,port,data_to_send):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
    s.connect((host,port)) 
    s.send(data_to_send) 

    data = s.recv(size)
    
    s.close()
    return data


host = 'block335046-zme.blueboxgrid.com' 
port = 50006
listen_port=50007
size = 1024 
backlog = 5
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind(('localhost',listen_port))
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



nargs = len(sys.argv)
if nargs > 1:
    host = sys.argv[1]
if nargs > 2:
    port = int(sys.argv[2])

input_string=''
print 'Enter the text to send(just hit enter to stop):'
while input_string!='\n':
    response=''
    if input_string!='':
        
        response=send_data(host,port,input_string)
    
    input_string=''
    
        
    

  

    
    inputready,outputready,exceptready = select.select(input,[],[],timeout)
    
        # timeout
        


    for s in inputready:
        
        if s == server:
            # handle the server socket
            
            client, address = server.accept()
            
                        
            input.append(client)

           
            

        elif s == sys.stdin:
            # handle standard input
            junk = sys.stdin.readline()
            
            input_string=junk
            
           

        elif s: # client socket


            data = s.recv(size)
           
            if data:
                print
                print  data.strip('\n')
                
                print
                print 'Enter the text to send(just hit enter to stop):'
                
                s.send('200')
            else:
                s.close()
                
                input.remove(s)
                s.close()

print "Chat client exited"
print
print
