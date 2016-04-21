#!/usr/bin/env python
import sys

#Unsanitezed settings input is considered a non-issue, if you can change the settings maliciously on purpose you can also just break anyway

ismain = ( __name__ == "__main__" )

settings = {}
try:
    for line in open ("settings.conf", "r"):
        key,value = map( lambda x: x.strip(), line.split("="))
        if ismain:
            print "export %s=%s" % (key,value)
        else:
            settings[key] = value
    
except:
    sys.stderr.write("%s\n" % "Invalid settings file, ABORTING...")
    exit()
