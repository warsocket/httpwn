#!/usr/bin/env python3

def application(environ, start_response):
    headers = [('Content-Type', 'text/plain')]
    headers.append(('Access-Control-Allow-Origin', f'{environ["wsgi.url_scheme"]}://httpwn.org'))

    start_response('200 OK', headers)
    return [environ["REMOTE_ADDR"].encode('ascii')]