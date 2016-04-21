#!/usr/bin/env python

#httpwn.org
#Copyright (C) 2016  Bram Staps
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
