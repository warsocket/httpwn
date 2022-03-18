#!/usr/bin/env python3
import os
import re
import json
import random
import time
from uuid import uuid4


import sys
# sys.stderr = sys.stdout
# print("Content-Type: text/plain\r\n\r")
# exit()

UUIDRGX = "^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
REDIRRGX = "^[0-9]-[0-9a-z]{16}-[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"


def rs():
	l = []
	for _ in range(16):
		l.append(random.choice("abcdefghijklmnopqrstuvwxyz0123456789"))
	return "".join(l)

print("Access-Control-Allow-Origin: *\r")

# if os.environ.get("HTTPS"):
# 	print("Access-Control-Allow-Origin: https://httpwn.org\r")
# else:
# 	print("Access-Control-Allow-Origin: http://httpwn.org\r")

print("Content-Type: text/json\r")
uuid = os.environ.get("HTTP_HOST").split(".", 1)[0]

# print(re.search(UUIDRGX[1:], uuid))

if os.environ.get("HTTP_HOST") == "httpwn.org":
	print("Status: 302 Found\r")
	print(f'Location: //0-{rs()}-{uuid4()}.in-addr.{os.environ.get("HTTP_HOST")}/dns\r')
	print("\r")


elif re.match(UUIDRGX, uuid): #full uuid match

	print("Status: 200 OK\r")
	print("\r")

	ipset = set()

	try:
		for file in os.listdir(f"/ramdisk/{uuid}/"):
			with open(f"/ramdisk/{uuid}/{file}", "r") as f:
				ipset.add(f.read())
	except FileNotFoundError:
		pass

	print( json.dumps(list(ipset)) )



elif re.match(REDIRRGX, uuid): #match with prefix
	print("Status: 302 Found\r")

	n = int(os.environ.get("HTTP_HOST")[0])
	if n < 9:
		print(f'Location: //{n+1}{os.environ.get("HTTP_HOST")[1:]}/dns\r')
	else:
		print(f'Location: //{os.environ.get("HTTP_HOST")[19:]}/dns\r')
	print("\r")

else:
	print("Status: 400 Bad Request\r\n\r")
	



