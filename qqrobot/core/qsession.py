# coding: utf-8

from utils import HTTPRequest, create_logger, bknHash


class BaseSession(object):
    """提供封装后的Web QQ接口
    """
    def __init__(self):
        self.http = HTTPRequest()
        self.log = create_logger()

    def get_QRcode(self):
        QRcode_url = (
            "https://ssl.ptlogin2.qq.com/ptqrshow?"
            "appid=501004106&e=0&l=M&s=5&d=72&v=4&t=0.1"
        )
        response = self.http.get(QRcode_url).content
        with open("./QRcode.png", 'w') as qrcode:
            qrcode.write(response)

        # TODO: async run
        QRcode("./QRcode.png").show()


