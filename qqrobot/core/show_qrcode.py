#!/usr/bin/env python
# coding:utf-8

from PIL import Image


class QRcode:
    def __init__(self, image, width=33, height=33):
        self.image = image
        self.width = width
        self.height = height

    def show(self):
        im = Image.open(self.image)
        im = im.resize((self.width, self.height), Image.NEAREST)
        text = ''
        for w in range(self.width):
            for h in range(self.height):
                res = im.getpixel((h, w))
                text += '  ' if res == 0 else '██'
            text += '\n'
        # TODO: 适配各平台
        print(text)
        return text
