#!/usr/bin/env python3
import settings
import re
import os
from os import path
from os import environ


dns_trailer = ".".join([settings.dnsbase, settings.domain])

def done():
	print("Status: 400 Parameters invalid")
	print("Content-Type: text/plain")
	print("")
	exit()

#parse parameter
if "&" in environ["QUERY_STRING"]: done()
if "=" not in environ["QUERY_STRING"]: done()
data = environ["QUERY_STRING"].split("=")
if len(data) != 2: done()
if data[0] != "dns": done()
dnskey = data[1]
if not re.match("^([a-zA-Z0-9][a-zA-Z0-9\\-]*)(\\.[a-zA-Z0-9][a-zA-Z0-9\\-]*)*$", dnskey): done() #correctish regex for domain name which prevents path traversal

#fetch data lines to display

tr = dns_trailer.split(".")
tr.reverse()
dnskeyrev = list(map(lambda x: x.lower(), dnskey.split("."))) # We will match for lowercase, as saved by dnsmon
dnskeyrev.reverse()
l = [settings.dnsmon] + tr + dnskeyrev
p = path.join(*l)


print("Status: 200")
print("Content-Type: text/plain")
print("")

files = []
for step in os.walk(p):
	prefix,_,filelist = step
	files += map(lambda x: path.join(prefix, x), filelist)

files.sort(key=lambda x: x.rsplit("/", 1)[-1])
files.reverse()
for file in files:
	with open(path.join(p, file), "r") as f: print(f.read())