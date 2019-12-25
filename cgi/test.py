#!/usr/bin/env python3
import sys
print("Status: 200")
print("Content-Type: text/plain")
print("")
print("-"*40)
x = sys.stdin.read()
print(len(x))
print("-"*40)
