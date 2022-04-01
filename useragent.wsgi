#!/usr/bin/env python3

def application(environ, start_response):
    headers = [('Content-Type', 'text/plain')]

    start_response('200 OK', headers)
    yield environ["HTTP_USER_AGENT"].encode('ascii')