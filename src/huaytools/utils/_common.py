#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Time:
    2022-08-30 10:28
Author:
    huayang (imhuay@163.com)
Subject:
    _common
"""
from __future__ import annotations

import logging


class CommonUtils:
    """"""

    @staticmethod
    def get_logger(name: str = None):
        """返回一个 logger"""
        from .python_utils import PythonUtils
        return logging.getLogger(name or PythonUtils.get_caller_name())


get_logger = CommonUtils.get_logger
