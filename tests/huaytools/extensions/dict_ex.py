#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Time:
    2022-09-16 17:07
Author:
    huayang (imhuay@163.com)
Subject:
    dict_ex
"""
from __future__ import annotations

# import os
# import sys
import unittest

# from typing import *
from huaytools.extensions import BunchDict


class TestBunchDict(unittest.TestCase):

    def test_base(self):
        x = BunchDict(a=1, b=2)
        self.assertEqual(x, {'a': 1, 'b': 2})

        x.c = 3
        self.assertIn('c', x)
        self.assertEqual(x['c'], x.c)

        x['d'] = {'foo': 6}
        self.assertIs(type(x.d), BunchDict)
        self.assertTrue(hasattr(x, 'd'))
        self.assertTrue(hasattr(x.d, 'foo'))

        x.c = {'bar': 8}
        self.assertIs(type(x.c), BunchDict)

        self.assertEqual(dir(x), ['a', 'b', 'c', 'd'])
        self.assertEqual(vars(x), {'a': 1, 'b': 2, 'c': {'bar': 8}, 'd': {'foo': 6}})

        with self.assertRaises(AttributeError):
            del x.a
            getattr(x, 'a')

        with self.assertRaises(AttributeError):
            x.__dict__ = {}  # noqa

        x.__doc__ = {'a': 1}
        self.assertIs(type(x.__doc__), BunchDict)

    def test_from_dict(self):
        y = {'foo': {'a': 1, 'bar': {'c': 'C'}}, 'b': 2}
        x = BunchDict.from_dict(y)
        self.assertEqual(y, x)
        self.assertEqual(x, BunchDict(y))

        x = BunchDict(y, d={'z': 26})
        self.assertEqual(x, {'foo': {'a': 1, 'bar': {'c': 'C'}}, 'b': 2, 'd': {'z': 26}})
        self.assertEqual(x.foo, {'a': 1, 'bar': {'c': 'C'}})
        self.assertEqual(x.foo.bar, {'c': 'C'})
        for it in [x.foo, x.foo.bar, x.d]:
            self.assertIs(type(it), BunchDict)
