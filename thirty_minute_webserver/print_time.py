
import datetime
now = datetime.datetime.now()

print "<H3>THE CURRENT TIME IS<H3>"
print "<H1>" + now.strftime("%A,  %B %d %Y %I:%M:%S %p") + "</H1>"

