#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Time:
    2022-09-06 11:04
Author:
    huayang (imhuay@163.com)
Subject:
    python_utils
"""
from __future__ import annotations

import inspect
import unittest

from huaytools.utils import PythonUtils


class TestPythonUtils(unittest.TestCase):
    """"""

    def test_get_frame(self):
        """"""
        frame = PythonUtils.get_frame()
        self.assertEqual(self.test_get_frame.__name__, frame.f_code.co_name)

        frame2 = inspect.currentframe()
        self.assertTrue(frame2 is frame)

        frame3 = PythonUtils.get_frame(1)
        self.assertTrue(frame3 is frame.f_back)

    def test_get_caller_name(self):
        """"""

        def foo():
            caller_name = PythonUtils.get_caller_name()
            return caller_name

        name = foo()
        self.assertEqual(self.test_get_caller_name.__name__, name)

        name = PythonUtils.get_caller_name(0)
        self.assertEqual(self.test_get_caller_name.__name__, name)
