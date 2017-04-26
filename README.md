暂时只考虑支持 Python3

```
$ pip install -r requirements.txt
$ python cli.py
```

暂时性提供的简单扩展方式：
```python

from cli import bot, run

# 注册消息，函数返回值即为回复
@bot.register_msg("这里是收到的消息内容")
def hello():
    return "返回值即为回复"

# 如，对别人发过来的 hello 要回复 hello world，可以这么做
@bot.register_msg('hello')
def reply():
    return "hello world"

# 运行
run()
```
