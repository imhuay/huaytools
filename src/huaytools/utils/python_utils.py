#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Time:
    2022-09-06 10:57
Author:
    huayang (imhuay@163.com)
Subject:
    python_utils
"""
from __future__ import annotations

import os
# import sys
# import json
import inspect


# from typing import *
# from pathlib import Path


class PythonUtils:
    """"""

    @staticmethod
    def get_frame(level: int = 0):
        """
        Examples:
            >>> def foo():
            ...     f = PythonUtils.get_frame()
            ...     return f.f_code.co_name
            >>> foo()
            'foo'
        """
        assert level >= 0
        frame = inspect.currentframe()  # 获取当前 frame，即 `get_frame` 的 frame
        for _ in range(level + 1):  # 向上逐级回溯调用者的 frame
            frame = frame.f_back

        return frame

    @staticmethod
    def get_caller_name(level: int = 1) -> str:
        """
        获取调用者的名字；

        使用场景：
            假设 foo 内部调用了 get_caller_name，则 get_caller_name 默认（level=1）会返回调用了 foo 的对象名；
            如果调用 foo 的对象是一个方法/模块/类，则返回该相应的的方法名/模块名/类名；

        Args:
            level: 回溯层级，默认为 1；

        Examples:
            >>> def foo():  # 在 bar 内部获取调用自身的方法名
            ...     name = PythonUtils.get_caller_name()  # 返回调用了 bar 的对象名
            ...     print(f'{name} called foo.')
            >>> def zoo():
            ...     return foo()
            >>> zoo()
            zoo called foo.

            >>> class T:
            ...     default = {'a': 1, 'b': 2}
            ...     def _get_attr(self):
            ...         name = PythonUtils.get_caller_name()
            ...         return self.default[name]
            ...     @property
            ...     def a(self):
            ...         # return default['a']
            ...         return self._get_attr()
            >>> t = T()
            >>> t.a
            1
        """
        assert level >= 0
        frame = PythonUtils.get_frame(level + 1)
        co_name = frame.f_code.co_name

        # 当调用方是一个模块，此时返回模块的文件名
        if co_name == '<module>':
            return os.path.basename(frame.f_code.co_filename)

        return co_name


class __Test:

    def __init__(self):
        import time
        from typing import Callable

        for k, v in self.__class__.__dict__.items():
            if k.startswith('_test') and isinstance(v, Callable):
                print(f'\x1b[32m=== Start "{k}" {{\x1b[0m')
                start = time.time()
                v(self)
                print(f'\x1b[32m}} End "{k}" - Spend {time.time() - start:3f}s===\x1b[0m\n')

    def _test_doctest(self):  # noqa
        import doctest
        doctest.testmod()

    def _test_xxx(self):  # noqa
        pass


if __name__ == '__main__':
    """"""
    __Test()
