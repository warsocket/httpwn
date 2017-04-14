#!/usr/bin/env python

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


# TODO 
# safe cookie parsing function 
# Etag for revalidate_cache_headers (EG: sha256 as etag for the requests file) 
# Protect agains ppl who jam server by connecting and not completing the http request (just accept x alive connecitons per ip, and maybe limit the request time to 1 sec)
# Make sure server can start form all directories

import sys
import os
import pwd
import sqlite3
import time
import selector

import websocket # this does not import on demand because of chroot jail
from site_constructs import *
#from settings import settings


def log_request(lines):
    try:
        conn = sqlite3.connect(settings["logfilepath"])
        c = conn.cursor()
        c.execute("""
        create table if not exists 'visitors' 
        (
            timestamp float,
            ip text,
            port integer,
            secure integer,
            request text    
        );
        """)
        c.execute( "insert into visitors values(?,?,?,?,?)", ( time(), get_ip(), int(get_port()), int(is_secure()), "\n".join(lines) ) )
        conn.commit()
        conn.close()
    except: #if we cannot log we quit
        sys.stderr.write("%s\n" % "Failed to log visit, ABORTING...") 
        exit()    


#jail me
ids = pwd.getpwnam(settings["unpriviligeduser"]) #need this before chroot
os.chroot(settings["jaildir"])
os.chdir("/")

#drop privileges
try:
    os.setgid(ids.pw_gid)
    os.setuid(ids.pw_uid)
except:
    sys.stderr.write("%s\n" % "Failed to drop priviliges, ABORTING...") 
    exit() #no lesser priviliges no page

#touch files
with open(settings["requestlogpath"], "a") as f:
    pass

#http parsing
line = sys.stdin.readline().strip() #get request
try:
    method, url, version = line.split(" ")
except ValueError: #No HTTP no DEAL
    exit()


#Url handling
lines = [line]
headers = {}
while line:
    try:
        header, content = line.split(":",1)
        headers[header] = content.strip()
    except ValueError: #discard ValueErrors of mal formatted headers
        pass
    
    line = sys.stdin.readline().strip() #get request
    lines.append(line)

if "Content-Length" in headers:
    try:
        lines.append(sys.stdin.read(int(headers["Content-Length"])))
    except:
        exit() # funny stuff makes your connection dead eg: value errors    

if "Sec-WebSocket-Key" in headers: # oh goody, a websocket
	websocket.connection(method, url, version, headers)
	exit() #Its a websockjet so we dotn do HTTP stuff


log_request(lines) #always log before giving an answer

#bumping to sepcified servername
if settings["bumptoservername"] == "1":
    if "Host" in headers:
        if headers["Host"] not in [settings['servername'], settings['ipv4dnsrecord'], settings['ipv6dnsrecord']] :
            print "HTTP/1.1 302 FOUND"
            print "Location: %s://%s%s" % (proto_name(), settings["servername"], url)
            print ""
            exit()

#now delegate
selector._delegate(method, url, version, headers, lines)
