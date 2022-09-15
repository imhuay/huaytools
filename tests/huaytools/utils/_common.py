#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Time:
    2022-09-05 17:12
Author:
    huayang (imhuay@163.com)
Subject:
    _common
"""
from __future__ import annotations

from unittest import TestCase

from huaytools.utils import CommonUtils, code_timer


class TestCommonUtils(TestCase):  # noqa

    def test_get_logger(self):
        get_logger = CommonUtils.get_logger

        logger = get_logger()
        self.assertEqual(self.test_get_logger.__name__, logger.name)

        logger2 = get_logger(logger.name)
        self.assertTrue(logger2 is logger)


class TestCodeTimer(TestCase):

    def test_base(self):
        import time

        def func():
            print(func.__name__)
            time.sleep(1)

        print()
        code_timer()(func)()

        with code_timer():
            func()

        self.assertTrue(True)
