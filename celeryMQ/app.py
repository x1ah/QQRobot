#!/usr/bin/env python
# coding:utf-8

from celery import Celery

qqrobotMQ = Celery('celeryMQ.app', include=['qqrobot.core.qsession'])

qqrobotMQ.config_from_object('config.CeleryConfig')


if __name__ == "__main__":
    qqrobotMQ.start()
