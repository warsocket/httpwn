#!/usr/bin/env python3
import settings
import re
from os import listdir
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
l = [settings.dnsmon] + tr + [dnskey]
p = path.join(*l)


print("Status: 200")
print("Content-Type: text/plain")
print("")
for file in listdir(p):
	with open(path.join(p, file), "r") as f: print(f.read())

