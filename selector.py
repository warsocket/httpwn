#httpwn.org
#Copyright (C) 2016  Bram Staps
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU Affero General Public License as
#published by the Free Software Foundation, either version 3 of the
#License, or (at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU Affero General Public License for more details.
#
#You should have received a copy of the GNU Affero General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

import re
l_and = lambda x,y : x and y

#Method, URL, HttpVersion, -> function
sites=[]

def _delegate(method, url, version, headers, lines):
    for re_method, re_url, re_version, func in sites:
        if reduce(l_and, map(bool, [re_method.match(method), re_url.match(url), re_version.match(version)])):
            print "HTTP/1.1 200 OK"
            func(method, url, version, headers, lines)
            exit(0)

    #if we get here no matches have been found
    print "HTTP/1.1 404 Not Found"
    print "Connection: close"
    print "Content-Type: text/html"
    print """
    <html>
    <head />
    <body style="background-color:black">
    <div style="text-align:center">
    <font style="font-family:Monospace;font-size:500%;color:#0F0"><b>404</b></font>
    </div>
    </body>
    </html>
    """
    exit(0)

#now the apges may be loaded
ALL = re.compile("")
GET = re.compile("(^(GET)|(HEAD)$)")
POST = re.compile("^POST$")

import pages
pages._sites(sites,ALL,GET,POST,re.compile)
