#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Time:
    2022-09-13 16:22
Author:
    huayang (imhuay@163.com)
Subject:
    meta_ex
"""
from __future__ import annotations

# import os
# import sys
# import json
import unittest

# from typing import *
from concurrent.futures import ThreadPoolExecutor, as_completed

from huaytools.extensions import SingletonMeta
from huaytools.extensions import SingletonABC


# from huaytools.utils import get_logger
# logger = get_logger()


class TestSingletonMeta(unittest.TestCase):
    class A(metaclass=SingletonMeta):
        def __init__(self, value=None):
            self.value = value

    def test_base(self):
        self.assertIs(self.A(), self.A())

    def test_thread_safe(self):
        """
        记录一个测试问题：
            在测试线程不安全时（通过 time.sleep），单独运行这条测试会得到期望的结果（期望不通过）；
            但是直接运行整个文件时，会得到相反的结果；
        """
        instances = []
        n_instance = 100
        with ThreadPoolExecutor(max_workers=10) as executor:
            todo = []
            for i in range(n_instance):  # 模拟多个任务
                future = executor.submit(self.A, value=i)
                todo.append(future)

            for future in as_completed(todo):  # 并发执行
                instances.append(future.result())

        # print(instances[:3])
        for i in instances:
            self.assertIsNotNone(i)

        singleton = instances[0]
        for i in instances:
            self.assertIs(i, singleton)

    # def test_time_cost(self):
    #     """
    #     测试显示加入两次判断，是否能够提升速度
    #     """
    #     import time
    #     from threading import Lock
    #
    #     class _SingletonMeta(type):
    #         _instances = dict()
    #         _lock = Lock()
    #
    #         def __call__(cls, *args, **kwargs):
    #             # 去除第一次判断
    #             # if cls not in cls._instances:
    #             with cls._lock:
    #                 if cls not in cls._instances:  # 第二次判断：防止实例被多次创建
    #                     # import time
    #                     # time.sleep(1)  # test thread safety
    #                     cls._instances[cls] = super().__call__(*args, **kwargs)
    #             return cls._instances[cls]
    #
    #     class A(metaclass=SingletonMeta):
    #         pass
    #
    #     class B(metaclass=_SingletonMeta):
    #         pass
    #
    #     n_time = 100000
    #     tmp = []
    #     start = time.time()
    #     for _ in range(n_time):
    #         tmp.append(A())
    #     t1 = time.time() - start
    #     # print()
    #     # print(t1)
    #
    #     tmp = []
    #     start = time.time()
    #     for _ in range(n_time):
    #         tmp.append(B())
    #     t2 = time.time() - start
    #     # print(t2)
    #     self.assertLess(t1, t2)


class TestSingletonABC(TestSingletonMeta):
    class A(SingletonABC):
        def __init__(self, value=None):
            self.value = value

    def test_base(self):
        super().test_base()

    def test_thread_safe(self):
        super().test_thread_safe()

    def test_time_cost(self):
        pass
