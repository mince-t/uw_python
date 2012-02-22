"""
Minimal WSGI + forms demo, with persistence

Send HTML page that echoes message from HTTP request
To get started, point browser at echo_wsgi.html

Based on example in PEP 333, then add path and query processing
"""

import urlparse
from cgi import escape
# send one of these pages, depending on URL path

form_page = """<head>
<title>Echo request</title>
</head>
<body>
<form method="GET" action="echo_wsgi.py">
Message: <input type="text" name="message" size="40">
<input type="submit" value="Submit">
</form>
</body>
</html>
"""

#I chose to put my history in a scrollable list
#Start tag for form was missing, I added.
message_template = """
<html>
    <head>
        <title>Echo response</title>
    </head>
    <body>
        <form>
            Messages:<br>
            <select size="10" style="width:250px;">
%s
            </select>
        </form>
    </body>
</html>
"""

notfound_template = """
<html>
<head>
<title>404 Not Found</title>
</head>
<body>
404 %s not found
</form>
</body>
</html>
"""
input_history=[]
# must be named 'application' to work with our wsgi simple server
def application(environ, start_response): 
    status = '200 OK'
    response_headers = [('Content_type', 'text/HTML')]
    start_response(status, response_headers)
    # send different page depending on URL path
    path = environ['PATH_INFO'] 
    if path == '/echo_wsgi.html':
        page = form_page
    elif path == '/echo_wsgi.py':
        
        #parse the message and escape any HTML unfriendly chars
        option=escape(urlparse.parse_qs(environ['QUERY_STRING'])['message'][0])

        #make the message into an HTML option
        option="""                <option value="%s">%s</option>\n""" % (option,option)

        #add the the current message to our list of html options
        input_history.append(option)
        history_output=''

        #creat our list of messages sorted descending by order added
        for item in input_history:
            history_output = item + history_output
        page = message_template % (history_output)
        
    else:
        page = notfound_template % path
    return [ page ] # list of strings - must return iterable, not just a string
