## 使用
>暂时只考虑支持 Python3

```
$ pip install -r requirements.txt
$ python cli.py
```

## 扩展

暂时性提供的简单扩展方式：
```python

from qqrobot import bot, run

# 注册特定消息字段

# 注册消息，函数返回值即为回复
@bot.register_msg("这里是收到的消息内容")
def hello(msg):
    return "返回值即为回复"

# 如，对别人发过来的 hello 要回复 hello world，可以这么做
@bot.register_msg('hello')
def reply(msg):
    return "hello world"


# 拦截所有消息

@bot.register_msg("ALL")
def reply_all(msg):
    """接收到的所有消息将会加上 ALL 回复给发送者,
    单独注册的消息不受影响
    """
    return msg + "ALL"

# 运行
run()
```

## TODO
- [ ] 正则匹配消息
- [ ] 处理群消息，讨论组消息
- [ ] 获取联系人列表，QQ号，QQ群号回复，发送

## Features
- 自动回复
- 收集消息
