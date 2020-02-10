#!/usr/bin/env python3
#Usage pruneold.py dir age
#EG: pruneold.py /tmp/ 360 #prune all files in tmp olde rthen an hour
#Example crontab entry: * * * * * /var/www/server/pruneold.py /httpwnbus/dnsmon 3600

import sys
import os
import time
import shutil

os.chroot(sys.argv[1])
now = time.time()
for file in os.walk("/"):
    rootname, _, filenames = file
    for filename in map(lambda x: os.path.join(rootname, x), filenames):
        #print(filename)
        if filename == sys.argv[1]: continue #we dont prune the directory only its content
        if (now - os.path.getmtime(filename)) > int(sys.argv[2]): 
            try:
                shutil.rmtree(filename)
            except:
                os.remove(filename)

