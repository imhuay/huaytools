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

from huaytools import CodeTimer, get_logger


class TestCommonUtils(TestCase):  # noqa

    def test_get_logger(self):

        logger = get_logger()
        self.assertEqual(self.test_get_logger.__name__, logger.name)

        logger2 = get_logger(logger.name)
        self.assertTrue(logger2 is logger)


class TestCodeTimer(TestCase):

    def test_base(self):
        logger = get_logger()

        def func():
            pass

        CodeTimer(stream=logger.info)(func)()

        with CodeTimer(stream=logger.info):
            func()

        self.assertTrue(True)
