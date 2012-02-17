"""
This module will listen on the specified socket and
generate a web page for each request.  The generated
web page presents a form to search postings by author on
allseattletango.com through their exposed rss feed.
Their rss feed is converted to JSON via the feed parsor
library available at:

http://code.google.com/p/feedparser/downloads/list

"""
import time
import select
import socket
import sys
import feedparser
import sys
import urllib
from pprint import pprint

"""
    Search for posts on allseattletango.com from author user_name

    
"""

response_header="""HTTP/1.1 200 OK
Date: Fri, 17 Feb 2012 23:26:19 GMT
Content-Type: text/html; charset=UTF-8

"""
def get_ast_data(user_name):

    #Open the HTML template
    template_file=open('ast_feed.template')

    #Load template into memory
    template_text=template_file.read()
    template_file.close()
    html=""
    #Load the feed in JSON format
    d=feedparser.parse('http://allseattletango.com/mb/rss/')

    #Set character encoding for our page to utf-8
    #html=u'<meta http-equiv="content-type" content="text/html; charset=utf-8">'

    #List of autors for the HTML select on our generated page
    authors={}
    
    #Keep track of which option element should be selected
    selected=''
    post_num=1
    for entry in d.entries:


        
        
        if entry['author']==user_name:


            #time.strftime("%a %b %d %H:%M:%S %Y",entry['updated_parsed'])
            post_date=time.strftime("%a, %b %d %Y %I:%M:%S %p",entry['updated_parsed'])
            post_num+=1
            color=""
            if post_num % 2 == 0:
                color= 'white'
            else:
                color='#FFFF99'

            div_style="style='padding:10px;witdh:100%%;background-color:%s'" % color
            
            #Set the option element representing the author searched as selected
            selected='SELECTED'

            #Generate markup for our search results
            html += u"\n\t\t<div %s><h2>%s</h2>Posted on %s<br>%s\n\t\t</div>" % (div_style,entry['title'], post_date, entry['summary_detail']['value'].replace('\n','\n\t\t\t'))

        #Set the dictionary item for the author for our select list
        authors[entry['author']]="\t\t\t\t\t<option value='%s' %s >%s</option>\n" % (entry['author'],selected,entry['author'])

        #Clear the selected attribut
        selected = ''
        
    author_options=""
    #Generate the string that defines our options for our select list
    for author in authors:
        author_options+=authors[author]
        
    #Load our search results and our authors list into the HTML template
    html = template_text % (author_options,html)

    #Return our page in utf-8
    return html.encode( "utf-8" )


host = ''
listen_port = 8081

if len(sys.argv) > 1:
    listen_port = int(sys.argv[1])

backlog = 5
size = 1024

#tool up to listen for page requests
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((host,listen_port))

#let the user know what's going on
print '\n'*10
print '____________________________________________'
print '   ast_post_server'

print '   LISTENING LISTENING ON %s' % listen_port 

print '____________________________________________'
print '\n'*10

#start listening
server.listen(backlog)

timeout = 10 
input = [server,sys.stdin]
running = True

while running:
    
    inputready,outputready,exceptready = select.select(input,[],[],timeout)
    
    for s in inputready:
        #If a client hit our server
        if s == server:

            # handle the server socket
            client, address = server.accept()
            print
            print 'accepted connection from', address

            #Read the clients request
            data = client.recv(size)

            #If this isn't a null request
            if data:
                query=""

                #if there is data in the request
                if len(data.split('\r\n\r\n'))>0:
                    #if there is a name/value pair
                    if len(data.split('\r\n\r\n')[1].split('='))>1:
                        #parse the search term(author)
                        query=urllib.unquote_plus(data.split('\r\n\r\n')[1].split('=')[1])
                        print "searching for %s" % query

                #get all posts from the specified author
                client.send(response_header)
                client.send(get_ast_data(unicode(query)))
                client.close()
            

        elif s == sys.stdin:
            # handle standard input
            #junk = sys.stdin.readline()
            #running = False
            #print 'Input %s from stdin, exiting.' % junk.strip('\n')
            pass
