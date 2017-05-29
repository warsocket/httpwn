#!/usr/bin/env bash

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
cd $(dirname $0)

$(./settings.py) # load settings

if [ "$1" ==  "start" ]
then
    #IPv4+6
    if [ -f $httppid ]
    then
        echo http server already running
    else
        $socatpath TCP6-LISTEN:80,reuseaddr,ipv6only=0,fork,crnl EXEC:./main.py 2>> $httplog &
        echo -n $! > $httppid
    fi

    if [ -f $httpspid ]
    then
        echo https server already running
    else
        $socatpath OPENSSL-LISTEN:443,reuseaddr,pf=ip6,ipv6only=0,fork,crnl,cert=$certfile,method=$sslmethod,verify=0,ciphers=$sslciphers EXEC:./main.py 2>> $httpslog &
        echo -n $! > $httpspid
    fi

elif [ "$1" ==  "stop" ]
then
    #IPv4+6
    if [ -f $httppid ]
    then
        echo killing pid `cat $httppid`
        kill `cat $httppid`
        rm $httppid
    fi

    if [ -f $httpspid ]
    then
        echo killing pid `cat $httpspid`
        kill `cat $httpspid`
        rm $httpspid
    fi
    
elif [ "$1" ==  "status" ]
then
    #IPv4+6
    if [ -f $httppid ]
    then
        echo http server running under pid: `cat $httppid`
    else
        echo http server not runnig
    fi

    if [ -f $httpspid ]
    then
        echo https server running under pid: `cat $httpspid`
    else
        echo https server not runnig
    fi

else
    echo "use $0 (start|stop|status)"
    #$socatpath OPENSSL-LISTEN:443,reuseaddr,fork,crnl,cert=$certfile,method=$sslmethod,verify=0,ciphers=$sslciphers EXEC:./main.py #test line
fi


