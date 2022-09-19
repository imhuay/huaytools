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

from huaytools import PythonUtils


class TestPythonUtils(unittest.TestCase):
    """"""

    def test_get_version(self):
        v = PythonUtils.get_version()
        self.assertEqual(3, len(v))
        self.assertGreaterEqual(3, v[0])

    def test_get_frame(self):
        frame = PythonUtils.get_frame()
        self.assertEqual(self.test_get_frame.__name__, frame.f_code.co_name)

        frame2 = inspect.currentframe()
        self.assertTrue(frame2 is frame)

        frame3 = PythonUtils.get_frame(1)
        self.assertTrue(frame3 is frame.f_back)

    def test_get_caller_name(self):
        def foo():
            caller_name = PythonUtils.get_caller_name()
            return caller_name

        name = foo()
        self.assertEqual(self.test_get_caller_name.__name__, name)

        name = PythonUtils.get_caller_name(0)
        self.assertEqual(self.test_get_caller_name.__name__, name)

    def test_get_lineno(self):
        expected_lno = 50
        lno = PythonUtils.get_lineno()
        self.assertEqual(expected_lno, lno)

        def foo():
            return PythonUtils.get_lineno(1)

        lno = foo()
        self.assertEqual(expected_lno + 6, lno)

    def test_get_annotation_names(self):

        class Demo:
            a: int
            b: str
            c = []

        names = PythonUtils.get_annotation_names(Demo)
        self.assertEqual(names, ['a', 'b'])

        names = PythonUtils.get_annotation_names(Demo())
        self.assertEqual(names, ['a', 'b'])
