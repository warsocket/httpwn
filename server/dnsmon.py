#!/usr/bin/env python2

#dnsecho
#Copyright (C) 2019  Bram Staps
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

import pwd
import socket
import struct
import os
import sys
import time
import datetime

dns_handlers = {
	1 : "A",
	28 : "AAAA",
	18 : "AFSDB",
	42 : "APL",
	257 : "CAA",
	60 : "CDNSKEY",
	59 : "CDS",
	37 : "CERT",
	5 : "CNAME",
	49 : "DHCID",
	32769 : "DLV",
	39 : "DNAME",
	48 : "DNSKEY",
	43 : "DS",
	55 : "HIP",
	45 : "IPSECKEY",
	25 : "KEY",
	36 : "KX",
	29 : "LOC",
	15 : "MX",
	35 : "NAPTR",
	2 : "NS",
	47 : "NSEC",
	50 : "NSEC3",
	51 : "NSEC3PARAM",
	61 : "OPENPGPKEY",
	12 : "PTR",
	46 : "RRSIG",
	17 : "RP",
	24 : "SIG",
	53 : "SMIMEA",
	6 : "SOA",
	33 : "SRV",
	44 : "SSHFP",
	32768 : "TA",
	249 : "TKEY",
	52 : "TLSA",
	250 : "TSIG",
	16 : "TXT",
	256 : "URI",
	255 : "*",
	252 : "AXFR",
	251 : "IXFR",
	41 : "OPT",
	3 : "MD",
	4 : "MF",
	254 : "MAILA",
	7 : "MB",
	8 : "MG",
	9 : "MR",
	14 : "MINFO",
	253 : "MAILB",
	11 : "WKS",
	32 : "NB",
	33 : "NBSTAT",
	10 : "NULL",
	38 : "A6",
	30 : "NXT",
	25 : "KEY",
	24 : "SIG",
	13 : "HINFO",
	17 : "RP",
	19 : "X25",
	20 : "ISDN",
	21 : "RT",
	22 : "NSAP",
	23 : "NSAP-PTR",
	26 : "PX",
	31 : "EID",
	32 : "NIMLOC",
	34 : "ATMA",
	42 : "APL",
	40 : "SINK",
	27 : "GPOS",
	100 : "UINFO",
	101 : "UID",
	102 : "GID",
	103 : "UNSPEC",
	99 : "SPF",
	56 : "NINFO",
	57 : "RKEY",
}

dns_classes = {
	1 : "IN",
	3 : "CH",
	4 : "HS",
}

def to_short(num):
	return struct.pack("!H", num)

def from_short(blob):
	return struct.unpack("!H", blob)[0]

def handle(data, address):
	QUESTION_OFFSET = 12

	trans_id = data[0:2]
	flags = data[2:4]
	questions = from_short(data[4:6])

	#skip 8 bytes dont care
	offset = QUESTION_OFFSET
	name = []

	#for x in xrange(questions):
	if questions != 1: return #dont aswer when more then 1 qeustion is sent
	while data[offset] != "\x00":
		length = ord(data[offset])
		offset += 1
		name.append(data[offset:offset+length])
		offset += length

	record_type = from_short(data[offset+1:offset+3])
	record_class = from_short(data[offset+3:offset+5])

	question_end = offset+1+2+2 #include 00 byte + include type + include class

	try:
		t = dns_handlers[record_type]
	except KeyError:
		t = record_type

	try:
		c = dns_classes[record_class]
	except KeyError:
		c = record_type

	n = ".".join(name)

	if "." in address[0]:
		ip = address[0].rsplit(":", 1)[-1]
	else:
		ip = address[0]

	d = datetime.datetime.now()
	print d, ip, c, t, n
	if path:
		parts = n.split(".")
		parts.reverse()
		partsum = []
		for part in parts:
			part = part.lower() #We log case insensitive, but since dns names are semantically case insessitive we lower here.
			partsum.append(part)
			p = os.path.join(path,*tuple(partsum))
			try:
				os.mkdir(p)
			except:
				pass
		partsum.append("{:0>26.6f}.txt".format(time.time()))
		p = os.path.join(path,*tuple(partsum))
		with open(p, "w") as f: f.write("{} {} {} {} {}".format(d, ip, c, t, n))


#main starts here
path = None
if len(sys.argv) == 2:
	path = sys.argv[1]
	try:
		os.mkdir(path)
	except: 
		pass

if path:
    os.chroot(path)
    path = "/"

sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
sock.bind(("::", 53))

while True:
	data, address = sock.recvfrom(0XFFFF)
	handle(data, address)
