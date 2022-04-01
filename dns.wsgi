#!/usr/bin/env python3
import os
import re
import json
import random
import time
from uuid import uuid4

def application(environ, start_response):
	UUIDRGX = "^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
	REDIRRGX = "^[0-9]-[0-9a-z]{16}-[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
	headers = []

	def rs():
		l = []
		for _ in range(16):
			l.append(random.choice("abcdefghijklmnopqrstuvwxyz0123456789"))
		return "".join(l)

	headers.append(('Access-Control-Allow-Origin','*'))
	headers.append(('Content-Type','text/json'))

	uuid = environ["HTTP_HOST"].split(".", 1)[0]

	if environ["HTTP_HOST"] == "httpwn.org":
		headers.append(('Location', f'//0-{rs()}-{uuid4()}.in-addr.{environ["HTTP_HOST"]}/dns'))
		start_response('302 Found', headers)


	elif re.match(UUIDRGX, uuid): #full uuid match

		ipset = set()

		try:
			for file in os.listdir(f"/ramdisk/{uuid}/"):
				with open(f"/ramdisk/{uuid}/{file}", "r") as f:
					ipset.add(f.read())
		except FileNotFoundError:
			pass

		start_response('200 OK', headers)
		yield json.dumps(list(ipset)).encode("ascii")



	elif re.match(REDIRRGX, uuid): #match with prefix
		n = int(environ["HTTP_HOST"][0])
		if n < 9:
			headers.append(('Location', f'//{n+1}{environ["HTTP_HOST"][1:]}/dns'))
		else:
			headers.append(('Location', f'//{environ["HTTP_HOST"][19:]}/dns'))
		
		start_response('302 Found', headers)

	else:
		start_response('400 Bad Request', headers)