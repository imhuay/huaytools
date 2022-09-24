#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Time:
    2022-09-13 16:20
Author:
    huayang (imhuay@163.com)
Subject:
    abc_ex
"""
from __future__ import annotations

# import os
# import sys
# import unittest
import abc

# from typing import *
from threading import Lock


class SingletonMeta(type):
    """
    实现单例模式的元类（线程安全）

    Examples:
        >>> class A(metaclass=SingletonMeta): pass
        >>> A() is A()
        True
    """
    _instances = dict()
    _lock = Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:  # 第一次判断，防止每次判断都执行锁操作
            with cls._lock:
                if cls not in cls._instances:  # 第二次判断：防止实例被多次创建
                    # import time
                    # time.sleep(1)  # test thread safety
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class SingletonABC(abc.ABC):
    """
    实现单例模式的抽象类（线程安全）

    Notes:
        与 SingletonMeta 的区别：
            SingletonMeta 对单例是否存在的判断发生在 __init__ 之前，
            而 SingletonABC 发生在 __init__ 之后；
        考虑以下代码：

        class A(metaclass=SingletonMeta):
            def __init__(self, v):
                self.v = v

        class B(SingletonABC):
            def __init__(self, v):
                self.v = v

        a1, a2, a3 = A(1), A(2), A(3)
        b1, b2, b3 = B(1), B(2), B(3)
        print(a1 is a2 is a3)  # True
        print(b1 is b2 is b3)  # True
        print(a3.v)  # 1，新的 v 未生效，说明 __init__ 没有执行
        print(b1.v)  # 3，新的 v 生效了，可见已经执行了 __init__

    Examples:
        >>> class A(SingletonABC): pass
        >>> A() is A()
        True
    """
    _instance: SingletonABC
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        # try:
        #     return cls._instance
        # except AttributeError:
        #     cls._instance = super().__new__(cls)
        #     return cls._instance
        if not hasattr(cls, '_instance'):  # # 第一次判断，防止每次判断都执行锁操作
            with cls._lock:
                if not hasattr(cls, '_instance'):  # 第二次判断：防止实例被多次创建
                    # import time
                    # time.sleep(1)  # test thread safety
                    cls._instance = super().__new__(cls)
        return cls._instance
