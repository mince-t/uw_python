"""
echo client, usage:

 python echo_client.py <host> <port>

Both host and port are optional, defaults: localhost 50000
host must be present if you want to provide port
"""

import socket 
import sys

host = 'localhost' 
port = 50011
size = 1024 

nargs = len(sys.argv)
if nargs > 1:
    host = sys.argv[1]
if nargs > 2:
    port = int(sys.argv[2])


input_string=raw_input('Enter the text to send(just hit enter to stop):')
while input_string!='':
	s = socket.socket(socket.AF_INET, 
		              socket.SOCK_STREAM) 
	s.connect((host,port)) 
	s.send(input_string) 

	data = s.recv(size) 
	s.close() 
	print 'from (%s,%s) %s' % (host, port, data)
	input_string=raw_input('Enter the text to send(just hit enter to stop):')
