#!/usr/bin/env pypy

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

import SocketServer
import thread
import sys
import StringIO
import main
import socket
import ssl
from settings import settings

# def socket2file(sock, file):
# 	while True:
# 		file.write(sock.recv(0xFFFF))

# def file2socket(sock, file):
# 	while True:
# 		sock.sendall(file.read())

class V6Server(SocketServer.TCPServer, SocketServer.ForkingMixIn):
	address_family = socket.AF_INET6

class HTTPHandler(SocketServer.StreamRequestHandler):
	def handle(self):
		
		if sys.argv[-1] == "tls":
			sock = ssl.wrap_socket(self.request, certfile=settings["certfile"], server_side=True, ciphers=settings["sslciphers"])
		else:
			sock = self.request

		main.main(sock)
		sock.shutdown(socket.SHUT_RDWR)
		sock.close()

x = V6Server(("::", int(sys.argv[1])), HTTPHandler)


x.serve_forever()