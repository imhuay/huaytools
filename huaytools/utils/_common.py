#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Time:
    2022-08-30 10:28
Author:
    huayang (imhuay@163.com)
Subject:
    _common
"""
from __future__ import annotations

import time
import logging
import functools

from typing import Callable

from .python_utils import PythonUtils

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s@%(lineno)dL : %(message)s',
                    datefmt='%Y.%m.%d %H:%M:%S',
                    level=logging.INFO)
"""
References: https://docs.python.org/zh-cn/3/library/logging.html#logrecord-attributes
"""


class CommonUtils:
    """"""

    @staticmethod
    def get_logger(name: str = None):
        """返回一个 logger"""
        return logging.getLogger(name or PythonUtils.get_caller_name())


get_logger = CommonUtils.get_logger


class CodeTimer:
    name: str
    msg_start: str
    msg_end: str
    start: float
    stream: Callable

    def __init__(self, name: str = '', stream: Callable = print):
        """
        Args:
            name:
            stream:

        Examples:
            import time

            @code_timer()
            def foo():
                time.sleep(1)

            with code_timer('test'):
                time.sleep(1)

        TODO: add color
        """
        self.name = name
        # self.msg_start = msg_start or 'Start {name}{{'
        # self.msg_end = msg_end or '}} End - Spend {cost:.5f}s. \n'
        self.stream = stream

    def __call__(self, func):
        """"""
        if not self.name:
            self.name = func.__name__

        @functools.wraps(func)
        def wrap(*args, **kwargs):
            """"""
            self.info_start(self.name)
            self.start = time.time()
            func(*args, **kwargs)
            self.info_end()

        return wrap

    def info_start(self, name=''):
        if name:
            name = f' {name}'
        line = f' @{PythonUtils.get_lineno(2)}L'
        self.stream(f'Start{name}{line}{{')

    def info_end(self):
        cost = time.time() - self.start
        self.stream(f'}} End - Spend {cost:.5f}s. \n')

    def __enter__(self):
        self.info_start(self.name)
        self.start = time.time()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.info_end()


code_timer = CodeTimer()
