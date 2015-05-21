#!/usr/bin/env python3

import base64
import json
import urllib.request


def send_rpc(method, params):
    # send json-rpc calls to popcorntime

    # popcorntime configurations
    url = 'http://192.168.1.111:8008/jsonrpc'
    username = 'popcorn'
    password = 'popcorn'

    # json-rpc packer
    data = '''{{
                  "jsonrpc": "2.0",
                  "method": "{}",
                  "params": {},
                  "id": 1
              }}
           '''.format(method, params)

    print('==> : ' + data)
    data = data.encode()

    # basic authorization
    auth_string = base64.b64encode(('{}:{}'.format(
                                    username, password)).encode()).decode()

    req = urllib.request.Request(url, data)
    req.add_header('Content-Type', 'application/json')
    req.add_header('Authorization', 'Basic {}'.format(auth_string))

    res = urllib.request.urlopen(req)
    token_dict = json.loads(res.read().decode())
    print('<== : ' + str(token_dict))


def popcorn_play(magnet):
    print('Sending RPC calls to popcorntime ...')
    send_rpc('ping', '{}')
    try:
        send_rpc('ping', '{}')
    except:
        print("Unable to ping popcorntime")
        return

    send_rpc('startstream',
             '''{{
                    "imdb_id": "",
                    "torrent_url": "{}",
                    "backdrop": "",
                    "subtitle": "",
                    "selected_subtitle": "",
                    "title": "",
                    "quality": "",
                    "type": ""
                }}'''.format(magnet))


if __name__ == '__main__':
    popcorn_play('magnet:?xt=urn:btih:AGMTNAVY5XNEB6RT35IYVSJL7YRHCTVS')
