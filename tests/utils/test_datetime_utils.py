#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Time:
    2022-11-07 18:57
Author:
    huayang (imhuay@163.com)
Subject:
    test_datetime_utils
"""
from __future__ import annotations

# import os
# import sys
# import json
# import unittest

# from typing import *
# from pathlib import Path
# from collections import defaultdict

from datetime import datetime, timezone, timedelta
from huaytools.utils.datetime_utils import DatetimeUtils


class TestDatetimeUtils:

    def test_bjs(self):
        dt_utc = datetime.now(timezone(timedelta(hours=0)))
        dt_bjs = DatetimeUtils.as_bjs(dt_utc)

        assert dt_bjs.hour == dt_utc.hour + 8
