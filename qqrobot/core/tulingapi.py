#!/usr/bin/env python
# encoding: utf-8

import json
import requests

key = "60e5be58b171439cadcdfe2151c0eba9"
url = 'http://www.tuling123.com/openapi/api'
def tuling(info, userid = 0):
    message = {
        "key": key,
        "info": info,
        "userid": userid
    }
    send_message = requests.post(url,message).json()
    send = send_message['text']
    if 'list' in send_message:
        send = send + send_message['list']
    if '抽签' in info:
        send = "我才不要变成像kiko那样的神棍！loli不抽签！"
    return send

def robot_name():
    return 'loli'
