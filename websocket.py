import hashlib
import base64
import sys
import time

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
		
