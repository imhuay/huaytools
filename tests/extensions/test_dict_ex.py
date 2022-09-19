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

import json
# import os
# import sys
import unittest

# from typing import *
from dataclasses import dataclass, fields, field

from huaytools.extensions import BunchDict, DataclassDict


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
        self.assertEqual(str(x), "{'a': 1, 'b': 2, 'c': {'bar': 8}, 'd': {'foo': 6}}")

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

    def test_to_dict(self):
        y = {'foo': {'a': 1, 'bar': {'c': 'C'}}, 'b': 2}
        x = BunchDict(y).to_dict()
        self.assertEqual(x, y)
        self.assertIs(type(x), dict)


class TestDataclassDict(unittest.TestCase):

    @dataclass
    class Features(DataclassDict):
        a: int
        b: str = 'B'
        c: list = field(default_factory=list)

    def test_base(self):
        f = self.Features(a=1)
        self.assertTrue(f.a == f['a'] == 1)
        self.assertEqual(json.dumps(f), '{"a": 1, "b": "B", "c": []}')
        self.assertEqual(f, {'a': 1, 'b': 'B', 'c': []})
        self.assertEqual(vars(f), {'a': 1, 'b': 'B', 'c': []})

        field_names = [i.name for i in fields(f)]
        self.assertEqual(field_names, ['a', 'b', 'c'])

        f.a = ten = 10
        self.assertEqual(f.a, ten)
        self.assertEqual(f['a'], ten)

        f['b'] = bar = 'Bar'
        self.assertEqual(f.b, bar)
        self.assertEqual(f['b'], bar)

        f['d'] = 42
        with self.assertRaises(AttributeError):
            getattr(f, 'd')

        f.pop('d')
        f.c.append('Foo')
        self.assertEqual(json.dumps(f), '{"a": 10, "b": "Bar", "c": ["Foo"]}')

        f.__doc__ = 'doc'
        self.assertEqual(f.__doc__, 'doc')
