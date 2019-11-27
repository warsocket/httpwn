#!/usr/bin/env python3
import sys
print("status: 200 OK")
print("Content-Type: text/plain")
print("")
print("-"*40)
x = sys.stdin.read()
print(len(x))
print("-"*40)