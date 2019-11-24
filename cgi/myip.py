#!/usr/bin/env python3
import os
import sys


print("Response: 200")
print("Content-Type: text/plain")
print("")
try:
	print(os.environ["REMOTE_ADDR"])
except:
	print()




