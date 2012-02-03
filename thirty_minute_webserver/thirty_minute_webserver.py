#
# ws30 -- the thirty minute web server
# author: Wilhelm Fitzpatrick (rafial@well.com)
# date: August 3rd, 2002
# version: 1.0
#
# Written after attending a Dave Thomas talk at PNSS and hearing about
# his "write a web server in Ruby in one hour" challenge.
#
# Actual time spent:
#  30 minutes reading socket man page
#  30 minutes coding to first page fetched
#   3 hours making it prettier & more pythonic
#
# updated for UW Internet Programming in Python, by Brian Dorsey
#

import os, socket, sys,subprocess
# Default server and port
defaults = ['', '8080']
mime_types = {'.jpg' : 'image/jpg', 
            '.gif' : 'image/gif', 
            '.png' : 'image/png',
            '.html' : 'text/html',
            '.py' : 'text/html',
            '.pdf' : 'application/pdf'}
response = {}

response[200] =\
"""HTTP/1.0 200 Okay
Server: ws30
Content-type: %s

%s
"""

response[301] =\
"""HTTP/1.0 301 Moved
Server: ws30
Content-type: text/plain
Location: %s

moved
"""

response[404] =\
"""HTTP/1.0 404 Not Found
Server: ws30
Content-type: text/plain

%s not found
"""

response[500] =\
"""HTTP/1.0 500 Internal Server Error
Server: ws30
Content-type: text/plain

%s 
"""

DIRECTORY_LISTING =\
"""<html>
<head><title>%s</title></head>
<body>
<a href="%s..">..</a><br>
%s
</body>
</html>
"""

DIRECTORY_LINE = '<a href="%s">%s</a><br>'
host_name=""
def server_socket(host, port):
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)
    return s

def listen(s):
    connection, client = s.accept()
    return connection.makefile('r+')

def get_request(stream):
    method = None
    while True:
        line = stream.readline()
        
        if not line.strip(): 
            break
        elif not method: 
            method, uri, protocol = line.split()
    return uri

def list_directory(uri):
    entries = os.listdir('.' + uri)
    entries.sort()
    return DIRECTORY_LISTING % (uri, uri, '\n'.join(
        [DIRECTORY_LINE % (e, e) for e in entries]))

def get_file(path):
    f = open( path)
    
    try: 
        return f.read()
    finally: 
        f.close()

def get_content(uri):
    
    try:
        path = '.' + uri
        if os.path.isfile(path):
            
            if len(path)>3:
                if path[-3:]=='.py':
                    print"executing: %s" % uri
                    if path[path.rfind('/')+1:] != 'thirty_minute_webserver.py':
                        
                        #Launch a python module in a new sub-process
                       
                        process = subprocess.Popen(['python', path], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        process_result=process.communicate()
                        process_out=process_result[0]
                        process_err=process_result[1]
                        if process_err:
                            print "     ERROR: \n%s\n" % process_err
                        if not process_err:
                            
                            return (200, get_mime(uri),process_out )
                        else:
                            
                            return (500, "     ERROR:\n   " + process_err)
                    else:
                        print"   cannot execute %s " % path
                        redirect_page="""<html><head><meta http-equiv="REFRESH" content="10;url=http://""" + socket.getfqdn() + """:8080/"></head><body><h2>You can't run thirty_minute_webserver.py from here</h2><img src='duh.jpg' /><h3>redirecting to index in 10 ...</h3></body></html>"""
                        return (200, get_mime(uri),redirect_page )
                else:
                    print 'fetching : %s' % uri
                    return (200, get_mime(uri), get_file(path))
            else:
                return (200, get_mime(uri), get_file(path))
        if os.path.isdir(path):
            if(uri.endswith('/')):
                return (200, 'text/html', list_directory(uri))
            else:
                return (301, uri + '/')
        else: return (404, uri)
    except IOError, e:
        return (404, e)

def get_mime(uri):
    return mime_types.get(os.path.splitext(uri)[1], 'text/plain')

def send_response(stream, content):

    stream.write(response[content[0]] % content[1:])

if __name__ == '__main__':
    args, nargs = sys.argv[1:], len(sys.argv) - 1
    host, port = (args + defaults[-2 + nargs:])[0:2]
    server = server_socket(host, int(port))
    print 'starting %s on %s...' % (host, port)
    try:
        while True:
            stream = listen (server)
            send_response(stream, get_content(get_request(stream)))
            stream.close()
    except KeyboardInterrupt:
        print 'shutting down...'
    server.close()

