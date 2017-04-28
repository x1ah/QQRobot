#!/usr/bin/python
# coding: utf-8

import sys
import time
from threading import Thread

from qqrobot.core.qsession import BaseSession
from qqrobot.core.utils import ControlModel
from celeryMQ.app import qqrobotMQ
from qqrobot.core.ControlModel import keywords,control

bot = BaseSession()

@qqrobotMQ.task
def add(x, b):
    x + b


@qqrobotMQ.task
def async_send_msg(msg, from_uin, msg_type, *args, **kw):
    bot.send_msg(msg, from_uin, msg_type, *args, **kw)

@bot.register_msg("test")
def test():
    return "test 测试"

@bot.register_msg("hello")
def test():
    return "Hello world!"

print(bot.msg_handle_map)

def run():
    global bot
    bot.log.info("扫描二维码")
    bot.get_QRcode()
    IS_LOGIN = False
    while not IS_LOGIN:
        time.sleep(1)
        res = bot.is_login().split(',')[-2]
        bot.log.info(res)
        IS_LOGIN = True if '登录成功' in res else False
    bot.log.info('获取ptwebqq...')
    bot.get_ptwebqq()
    bot.log.info('获取vfwebqq...')
    bot.get_vfwebqq()
    bot.log.info('获取psessionid...')
    bot.get_psessionid()
    bot.log.info('等待消息...')
    STOP = False
    IS_OPEN = True
    control_key = False
    while not STOP:
        time.sleep(0.5)
        try:
            msg = bot.poll()
            if msg:
                msg_content, from_uin, msg_type = msg
            else:
                continue
            key_message = keywords()
            print(control_key)
            print('Hello')
            print(key_message)
            print(key_message in msg)
            if key_message in msg:
                print(control_key)
                control_key = True
                print(control_key)
                break
            if (IS_OPEN is True) and ('STOP' not in msg_content):
                # msg = "{0}[{1}]".format(SEND_MSG, random.randint(0, 10))
                # send_status = bot.send_msg(msg, from_uin, msg_type)
                # LOG.info('回复 {0}: {1}'.format(from_uin, send_status))
                # async_send_msg.delay(msg_content, from_uin, msg_type)
                Thread(target=bot.send_msg, args=(msg_content, from_uin, msg_type)).start()
            elif 'STOP' in msg_content:
                bot.log.info('CLOSE...')
                bot.send_msg.delay('CLOSED', from_uin, msg_type)
                IS_OPEN = False
            elif 'START' in msg_content:
                LOG.info('STARTED')
                bot.send_msg.delay('OPENED', from_uin, msg_type)
                IS_OPEN = True
        except KeyboardInterrupt:
            bot.log.info('See You...')
            STOP = True
        except:
            bot.log.error(sys.exc_info())

    while control_key:
        time.sleep(0.5)
        try:
            msg = bot.poll()
            if msg:
                if msg[0] == '#':
                    msg = msg[1:]
                    control(msg)
                else:
                    print('Error use.')
                    continue
            else:
                continue
        except KeyboardInterrupt:
            bot.log.info('Out of control...')
            bot.log.info('See You...')
            control_key = False


if __name__ == "__main__":
    run()

