#!/usr/bin/env pypy3
import os

if os.environ.get("HTTPS"):
	print("Access-Control-Allow-Origin: https://httpwn.org\r")
else:
	print("Access-Control-Allow-Origin: http://httpwn.org\r")

print("Content-Type: text/plain\r\n\r")
print(os.environ.get('REMOTE_ADDR'))
