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
import ssl

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


def is_secure(sock):
    return type(sock) is ssl.SSLSocket

def proto_name(sock):
    return ["http", "https"][is_secure(sock)]

def get_ip(sock):

    def ip_str(ip):
        #assumes the trialing zeros of socat
        try:
            # if ip[:30] == "[0000:0000:0000:0000:0000:ffff":
            try:
                _, ipv4 = ip.split("::ffff:")
                return ipv4
            except:
                return ip
                                
        except:
            return ip

    return ip_str( sock.getpeername()[0] )

def get_port(sock):
    return sock.getpeername()[1]




def html_headers(fd):
    print >>fd, "Connection: close"
    print >>fd, "Content-Type: text/html"

def plaintext_headers(fd):
    print  >>fd, "Connection: close"
    print  >>fd, "Content-Type: text/plain"

def static_cache_headers(fd):
    print  >>fd, "cache-control: max-age=86400"

def revalidate_cache_headers(fd):
    print  >>fd, "cache-control: max-age=0,must-revalidate"

def no_cache_headers(fd):
    print  >>fd, "cache-control: no-store"

def prologue(fd, schema):
    print  >>fd, """
<html>
<head>
<link href="%s://%s/style.css" rel="stylesheet" type="text/css">
</head>
<body>
""" % (schema, settings['servername'])

def epilogue(fd):
    print  >>fd, """
</body>
</html>
"""
