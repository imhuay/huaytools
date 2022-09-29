#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Time:
    2022-09-29 17:37
Author:
    huayang (imhuay@163.com)
Subject:
    markdown_utils
"""
from __future__ import annotations

# import os
# import sys
# import json
# import unittest

# from typing import *
# from pathlib import Path
# from collections import defaultdict

from markdown.extensions.toc import slugify_unicode  # noqa


class MarkdownUtils:

    @staticmethod
    def slugify(head):
        return slugify_unicode(head, '-')
