#!/usr/bin/env python3

def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    if environ["wsgi.url_scheme"] == "https":
    	return [f'{environ["SSL_PROTOCOL"]} ({environ["SSL_CIPHER"]})'.encode('ascii')]
    else:
    	return [b'-']