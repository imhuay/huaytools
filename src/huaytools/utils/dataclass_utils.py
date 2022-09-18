#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Time:
    2022-09-16 20:09
Author:
    huayang (imhuay@163.com)
Subject:
    dataclass_utils
"""
from __future__ import annotations

# import os
# import sys
# import unittest

# from typing import *
from dataclasses import fields


class DataclassUtils:

    @staticmethod
    def get_field_names(class_or_instance):
        return [f.name for f in fields(class_or_instance)]
