#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import

from celery import current_app

__all__ = ['task_method']


class task_method(object):

    def __init__(self, task, *args, **kwargs):
        self.task = task

    def __get__(self, obj, type=None):
        if obj is None:
            return self.task
        task = self.task.__class__()
        task.__self__ = obj
        return task

