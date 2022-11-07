#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Time:
    2022-10-14 0:26
Author:
    huayang (imhuay@163.com)
Subject:
    datetime_utils
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


class DatetimeUtils:
    """"""

    BJS = timezone(
        timedelta(hours=8),
        name='Asia/Beijing',
    )

    SHA = BJS
    UTCp8 = BJS

    @staticmethod
    def as_bjs(dt: datetime) -> datetime:
        return dt.astimezone(DatetimeUtils.BJS)
