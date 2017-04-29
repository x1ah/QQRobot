# coding: utf-8

import os
import sys
import json
sys.path.insert(0, '../..')
import functools


# from celeryMQ.app import qqrobotMQ
from .utils import HTTPRequest, create_logger, bknHash
from .show_qrcode import QRcode
#from celeryMQ.reuse_methods import task_method


class BaseSession(object):
    """提供封装后的Web QQ接口
    """
    def __init__(self):
        self.http = HTTPRequest()
        self.log = create_logger()
        self.msg_handle_map = {}
        self.psessionid = None

    def get_QRcode(self):
        QRcode_url = (
            "https://ssl.ptlogin2.qq.com/ptqrshow?"
            "appid=501004106&e=0&l=M&s=5&d=72&v=4&t=0.1"
        )
        response = self.http.get(QRcode_url).content
        with open("./QRcode.png", 'wb') as qrcode:
            qrcode.write(response)

        # TODO:
        #   [ ] async run
        QRcode("./QRcode.png").show()
        os.remove('./QRcode.png')

    def is_login(self):
        """扫码登录轮循获取登录状态
        """
        url = ("https://ssl.ptlogin2.qq.com/ptqrlogin?"
               "ptqrtoken={0}&webqq_type=10&"
               "remember_uin=1&login2qq=1&aid=501004106&u1=http%3A%2F"
               "%2Fw.qq.com%2Fproxy.html%3Flogin2qq%3D1%26webqq_type%"
               "3D10&ptredirect=0&ptlang=2052&daid=164&from_ui=1&pttype=1&"
               "dumy=&fp=loginerroralert&action=0-0-8449&mibao_css=m_webqq&"
               "t=1&g=1&js_type=0&js_ver=10216&login_sig=&"
               "pt_randsalt=2".format(
                   bknHash(self.http.session.cookies.get('qrsig'), init_str=0)
               ))
        self.http.session.headers['Referer'] = (
            "https://ui.ptlogin2.qq.com/cgi-bin/login?daid=164&target=self&"
            "style=16&mibao_css=m_webqq&appid=501004106&enable_qlogin=0&"
            "no_verifyimg=1&s_url=http%3A%2F%2Fw.qq.com%2Fproxy.html&"
            "f_url=loginerroralert&strong_login=1&login_state=10&t=20131024001"
        )
        response = self.http.get(url).text
        self.Ptwebqq_url = response.split("','")[2]
        # TODO:
        #   [ ] 保存cookie至本地
#        self.save_cookies()
        return response

    def get_ptwebqq(self):
        """获取ptwebqq参数
        """
        self.http.get(self.Ptwebqq_url, timeout=60)
        self.ptwebqq = self.http.session.cookies['ptwebqq']
        return self.ptwebqq

    def get_vfwebqq(self):
        vfwebqq_url = ("http://s.web2.qq.com/api/getvfwebqq?"
                       "ptwebqq={0}&clientid=53999199&psessionid=&"
                       "t=0.1".format(self.ptwebqq))
        self.http.session.headers['Referer'] = \
            "http://s.web2.qq.com/proxy.html?v=20130916001&callback=1&id=1"
        self.http.session.headers['Origin'] = 'http://s.web2.qq.com'
        vfw_res = self.http.get(vfwebqq_url, timeout=60).text
        self.vfwebqq = json.loads(vfw_res)['result']['vfwebqq']
        return self.vfwebqq

    def get_psessionid(self):
        api_url = 'http://d1.web2.qq.com/channel/login2'
        self.http.session.headers.update(
            {
                'Host': 'd1.web2.qq.com',
                "Origin": "http://d1.web2.qq.com",
                "Referer": (
                    "http://d1.web2.qq.com/proxy.html?"
                    "v=20151105001&callback=1&id=2")
            }
        )
        form_data = {
            'r': json.dumps(
                {
                    "ptwebqq": self.ptwebqq,
                    "clientid": 53999199,
                    "psessionid": '',
                    "status": "online"
                }
            )
        }
        pse_res = self.http.post(api_url, data=form_data).text
        result = json.loads(pse_res)['result']
        self.psessionid, self.uin = result['psessionid'], result['uin']
        return self.psessionid

    def parse_poll_res(self, msg):
        if 'error' in msg:
            if '103' in msg:
                return ('请登录Web QQ确定能收到消息再重新启动', 0, '')
            else:
                return
        msg_dict = json.loads(msg)
        tmp_res = msg_dict.get('result')[0].get('value')
        msg_content = tmp_res.get('content')[-1]
        from_uin = tmp_res.get('from_uin')
        msg_type = msg_dict.get('result')[0].get('poll_type')
        return (msg_content, from_uin, msg_type)

    def poll(self):
        poll_url = 'http://d1.web2.qq.com/channel/poll2'
        form_data ={'r': json.dumps(
            {
                "ptwebqq": self.ptwebqq,
                "clientid": 53999199,
                "psessionid": self.psessionid,
                "key": ''
            })}
        poll_res = self.http.post(poll_url, data=form_data, timeout=30).text
        fmsg = self.parse_poll_res(poll_res) # 解析轮循结果
        if fmsg:
            self.log.info("{0} 发来一条消息: {1}".format(fmsg[1], fmsg[0]))
        return fmsg

    def send_msg(self, msg: str, receive_id: int, msg_type: str, *args, **kw) -> str:
        if msg_type == 'message':
            send_url = 'http://d1.web2.qq.com/channel/send_buddy_msg2'
            # TODO:
            #   [x] 注册消息优先级，优先回复单独注册的消息内容
            #   [ ] 添加正则匹配系统，注册消息可使用正则表达式
            if msg in self.msg_handle_map.keys():
                _tmp_func = self.msg_handle_map.get(msg)
            else:
                # 注册使用 ALL 即注册所有消息, 默认回复原消息
                _tmp_func = self.msg_handle_map.get('ALL', (lambda x: x))
            msg = (
                lambda func, arg: func(arg)
            )(_tmp_func, msg)
            form_data = {
                'r': json.dumps({
                    'to': receive_id,
                    'content': json.dumps(
                        [msg,
                         ["font", {'name': "宋体", "size": 10,
                                    "style": [0, 0, 0], "color": "000000"}
                        ]]),
                    'face': 729,
                    'clientid': 53999199,
                    'msg_id': 34220099,
                    'psessionid': self.psessionid
                })
            }
            send_res = self.http.post(send_url, data=form_data).text
            self.log.info("回复{0}: {1}".format(receive_id, msg))
            return send_res
        else:
            # TODO:
            #   [ ] 根据消息类型分类处理
            return 'No Action'

    def register_msg(self, msg: str, type='message'):
        """提供消息注册
            提供 ALL 类型注册所有消息，即所有接收到的消息都会通过
            ALL 的注册函数，除了单独注册的消息，如：

            @bot.register_msg("ALL")
            def reply_any(msg):
                # 所有消息都会经过 reply_any 函数处理后回复
                return msg + "all append me"

            @bot.register_msg("hello", type='message')
            def hello(msg):
                '''函数返回值即回复内容
                '''
                # some other action
                return "reply hello"

        """
        def handle(func) -> None:
            # @functools.wraps(func)
            # def wrap(*args, **kw):
            # TODO:
            #   [ ] 更完善的消息处理机制
            # 此处应该在 send_msg 方法内处理回复，send_msg 为异步方法，优化性能
            self.msg_handle_map[msg] = func
        return handle
