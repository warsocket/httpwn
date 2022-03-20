#!/usr/bin/env python3
import sys
import re
import os
import time

#if it ends with regex its fine
UUIDRGX = "(.*)([0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12})$" 
DOMAIN = "in-addr.httpwn.org"

rgx = re.compile(UUIDRGX)


def out(x):
	print(x)
	sys.stdout.flush()


# def request(qtype, qname):
# 	print(f"Request: {qtype} {qname}", file=sys.stderr)

def helo(version):
	if version == "1":
		out("OK	ready")
		sys.stdout.flush()
		# print("OK	ready", file=sys.stderr)
	else:
		out("FAIL")
		# print("FAIL", file=sys.stderr)


def q(qname, qclass, qtype, rid, remoteip):
	# out(f"DATA	{qname}	{qclass}	{qtype}	")
	# print(f"Request: {qtype} {qname}", file=sys.stderr)

	#normalise
	qname = qname.lower()

	if qname == DOMAIN:
		if qtype == "SOA": 
			out(f"DATA	{qname}	{qclass}	{qtype}	3600	-1	in-addr.httpwn.org nomail.httpwn.org 1647114958 1200 180 3600 0")
		else:
			out(f"DATA	{qname}	{qclass}	A	3600	-1	5.9.249.62")
			out(f"DATA	{qname}	{qclass}	AAAA	3600	-1	2a01:4f8:211:2669::62")

	elif (len(qname) > len(DOMAIN)) and (qname[-(len(DOMAIN)+1):] == f".{DOMAIN}"):

		if qtype == "SOA": 
			out(f"DATA	{qname}	{qclass}	{qtype}	3600	-1	in-addr.httpwn.org nomail.httpwn.org 1647114958 60 60 60 0")

		elif qname == f"_acme-challenge.{DOMAIN}":
			with open("/var/www/certbot-validation.txt", "r") as f:
				for key in f:
					key = key.rstrip()
					out(f"DATA	{qname}	{qclass}	TXT	60	-1	{key}")

		elif "." not in qname[:-len(f".{DOMAIN}")]:
			out(f"DATA	{qname}	{qclass}	A	60	-1	5.9.249.62")
			out(f"DATA	{qname}	{qclass}	AAAA	60	-1	2a01:4f8:211:2669::62")

			part = qname.split(".", 1)[0]
			m = rgx.match(part)
			if m:
				uuid = m.group(2)
				try:
					os.mkdir(f"/ramdisk/{uuid}")
				except FileExistsError: pass

				with open(f"/ramdisk/{uuid}/{time.time()}", "w") as f:
					f.write(remoteip)


	else:
		out("FAIL"); return

	out("END")


funcmap = { 
	"HELO": helo,
	"Q": q,
}



while True:
	line = sys.stdin.readline()#.rstrip()
	# sys.stderr.write("DEBUG: " + line)

	line = line.rstrip()
	# print(f"line: {line}", file=sys.stderr)

	if not line: break
	split = line.split("\t")

	try:
		funcmap[split[0]](*split[1:])
	except KeyError:
		out("FAIL")
		# print("FAIL", file=sys.stderr)
