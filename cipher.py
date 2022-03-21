#!/usr/bin/env python3
import os

print("Content-Type: text/plain\r\n\r")
if os.environ.get("HTTPS"):
	print(f'{os.environ.get("SSL_PROTOCOL")} ({os.environ.get("SSL_CIPHER")})' )
else:
	print("-")

# SSL_PROTOCOL