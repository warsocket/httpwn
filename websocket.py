import hashlib
import base64
import sys
import time
import struct

def sendText(data):
	TEXT_FRAME_FIN = 0x81
 	length = len(data)

	if length <= 0x7D: #7 bits size -2
		frame = struct.pack("!B", TEXT_FRAME_FIN) + struct.pack("!B", length) + data

	elif length > 0xFFFF: #64 bits size
		frame = struct.pack("!B", TEXT_FRAME_FIN) + struct.pack("!B", 0x7F) + struct.pack("!Q", length) + data

	else: #16 bits size
		frame = struct.pack("!B", TEXT_FRAME_FIN) + struct.pack("!B", 0x7E) + struct.pack("!H", length) + data
	
	#Yes this breaks if you transfer maore thren 16777216 TB in one text mesage, good luck!

	sys.stdout.write( frame )
	sys.stdout.flush()



def sendPing():
	sys.stdout.write( "\x89\x00" )
	sys.stdout.flush()


def connection(method, url, version, headers):
	#now we need to supply a nice answer for websocket
	#and then uso stdin and stdout to control our messages since SOCAT is handling our TCP and TLS

	WEBSOCKET_STATIC_EPILOGUE = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

	shash = hashlib.sha1()
	shash.update( headers['Sec-WebSocket-Key'] )
	shash.update( WEBSOCKET_STATIC_EPILOGUE )
	seckey = base64.b64encode(shash.digest())

	print "HTTP/1.1 101 Switching Protocols"
	print "Upgrade: websocket"
	print "Connection: Upgrade"
	print "Sec-WebSocket-Protocol: 1337"
	print "Sec-WebSocket-Accept: %s" % seckey
	print ""
	sys.stdout.flush()
		
	poll = 0
	while True:

		#poll for data
		# sendText("x")

		#time to send a ping
		poll += 1
		if poll > 25:
			sendPing()
			poll = 0

		time.sleep(0.1) #polling time
		
