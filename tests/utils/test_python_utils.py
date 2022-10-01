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

from pathlib import Path

from huaytools import PythonUtils

module_name = PythonUtils.get_caller_name(0)


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

        with self.assertRaises(ValueError):
            PythonUtils.get_frame(100)

    def test_get_caller_name(self):
        def foo():
            caller_name = PythonUtils.get_caller_name()
            return caller_name

        name = foo()
        assert name == self.test_get_caller_name.__name__

        name = PythonUtils.get_caller_name(0)
        assert name == self.test_get_caller_name.__name__

        assert module_name == Path(__file__).name

    def test_get_lineno(self):
        assert PythonUtils.get_lineno() == inspect.currentframe().f_lineno

        def foo():
            return PythonUtils.get_lineno(1)

        assert foo() == inspect.currentframe().f_lineno

    def test_get_annotation_names(self):
        class Demo:
            a: int
            b: str
            c = []

        names = PythonUtils.get_annotation_names(Demo)
        self.assertEqual(names, ['a', 'b'])

        names = PythonUtils.get_annotation_names(Demo())
        self.assertEqual(names, ['a', 'b'])
