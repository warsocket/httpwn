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

from urllib import quote, unquote
from time import time
import os
from settings import settings


def parse_cookies(cookie_string):
    c = {}
    try:
        cookies = cookie_string.strip().split(";")
        cookies = map( lambda x: x.strip(), cookies )
        filter( lambda x: bool(x), cookies )
        for cookie in cookies:
            name, val = cookie.split("=")
            name = name.strip()
            val = val.strip()
            c[name] = val
    except:
        return {} #broken cookie string means no cookies

    return c    


def is_secure():
   return int(os.environ["SOCAT_SOCKPORT"]) == 443

def proto_name():
    return ["http", "https"][is_secure()]
    
def get_ip():
    return os.environ["SOCAT_PEERADDR"]

def get_port():
    return os.environ["SOCAT_PEERPORT"]

def html_headers():
    print "Connection: close"
    print "Content-Type: text/html"

def plaintext_headers():
    print "Connection: close"
    print "Content-Type: text/plain"

def static_cache_headers():
    print "cache-control: max-age=86400"

def revalidate_cache_headers():
    print "cache-control: max-age=0,must-revalidate"

def no_cache_headers():
    print "cache-control: no-store"

def prologue():
    print """
<html>
<head>
<link href="%s://%s/style.css" rel="stylesheet" type="text/css">
</head>
<body>
""" % (proto_name(), settings['servername'])

def epilogue():
    print """
</body>
</html>
"""
