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
# robots.txt
# Move hide button
# bump all to httpwn.org
# Https
# Git link
# Disclosure link
#

import sys
import os
import pwd
import sqlite3
import time
import selector
from site_constructs import *
from settings import settings


def log_request(lines):
#    try:
    conn = sqlite3.connect(settings["logfilepath"])
    c = conn.cursor()
    c.execute("""
    create table if not exists 'visitors' 
    (
        timestamp float,
        osi_source text,
        request text    
    );
    """)
    c.execute( "insert into visitors values(?,?,?)", (time(), ":".join([get_ip(), get_port()]), "\n".join(lines) ) )
    conn.commit()
    conn.close()
#    except: #if we cannot log we quit
#        sys.stderr.write("%s\n" % "Failed to log visit, ABORTING...") 
#        exit()    


#jail me
ids = pwd.getpwnam("www-data") #need this before chroot
os.chroot(settings["jaildir"])

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
    if line: #dont freak out over white line
        try:
            header, content = line.split(":")
            headers[header] = content.strip()
        except ValueError: #discard ValueErrors of mal formatted headers
            pass
    
    line = sys.stdin.readline().strip() #get request
    lines.append(line)

log_request(lines) #always log before giving an answer

#now delegate
selector._delegate(method, url, version, headers, lines)
