#!/usr/bin/env python
# encoding: utf-8

import json
import requests

key = "dbe6a304823a4fdb9150cbf43779aaf5"
url = 'http://www.tuling123.com/openapi/api'
def tuling(info, userid):
    message = {
        "key": key,
        "info": info,
        "userid": userid
    }
    send_message = requests.post(url,message).json()
    send = send_message['text']
    if 'list' in send_message:
        send = send + send_message['list']
    return send
