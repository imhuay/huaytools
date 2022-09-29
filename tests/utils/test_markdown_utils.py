#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Time:
    2022-09-29 17:39
Author:
    huayang (imhuay@163.com)
Subject:
    test_markdown_utils
"""
from __future__ import annotations

# import os
# import sys
# import json
# import unittest

# from typing import *
# from pathlib import Path
# from collections import defaultdict

from huaytools.utils import MarkdownUtils


class TestMarkdownUtils:

    def test_slugify(self):
        head = 'Test Head Line'
        assert MarkdownUtils.slugify(head) == 'test-head-line'

        head_cn = 'Test 中文标题'
        assert MarkdownUtils.slugify(head_cn) == 'test-中文标题'

        head_cn = 'Test 中文标题，带有标点（括号）'
        assert MarkdownUtils.slugify(head_cn) == 'test-中文标题带有标点括号'
