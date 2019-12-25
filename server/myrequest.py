#!/usr/bin/env python3
import socketserver

class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.request.sendall( b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n" + self.request.recv(0xFFFF) )

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    # Create the server, binding to localhost on port 9999
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
    server.serve_forever()

