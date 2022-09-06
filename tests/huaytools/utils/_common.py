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
from unittest import TestCase

from huaytools.utils import CommonUtils


class TestCommonUtils(TestCase):  # noqa

    def test_get_logger(self):
        get_logger = CommonUtils.get_logger

        logger = get_logger()
        self.assertEqual(self.test_get_logger.__name__, logger.name)

        logger2 = get_logger(logger.name)
        self.assertTrue(logger2 is logger)
