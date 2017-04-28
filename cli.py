#!/usr/bin/python
# coding: utf-8

from qqrobot import bot, run

# 简易扩展 demo
@bot.register_msg("test")
def test(msg):
    """单独注册某个消息字段可以针对性回复，
    单独注册的消息字段优先级大于下面的所有消息拦截，所以会回复
    这个注册函数的结果
    """
    return "test 测试"


@bot.register_msg("ALL")
def reply(msg):
    """通过注册 ALL 消息字段，可以实现拦截所有消息，对所有消息处理
    进行处理后再统一回复，在这里，所有消息将会加上 append 字符串
    再回复，通过此机制，可以接入第三方 API，如图灵机器人，小冰之类
    """
    return msg + "append"



if __name__ == "__main__":
    run()
