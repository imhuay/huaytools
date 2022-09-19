#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Time:
    2022-09-18 20:12
Author:
    huayang (imhuay@163.com)
Subject:
    dataclass_utils
"""
from __future__ import annotations

# import os
# import sys
import unittest

# from typing import *

from huaytools import DataclassUtils


class TestDataclassUtils(unittest.TestCase):

    def test_get_field_names(self):
        from dataclasses import dataclass

        @dataclass
        class Demo:
            a: int
            b: str
            c = ...

        self.assertEqual(DataclassUtils.get_field_names(Demo), ['a', 'b'])
