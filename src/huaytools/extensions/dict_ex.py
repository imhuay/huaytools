#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Time:
    2022-09-16 15:32
Author:
    huayang (imhuay@163.com)
Subject:
    dict_ex
"""
from __future__ import annotations

# import os
# import sys
# import unittest

from typing import Mapping, Union, Any, Iterable
from dataclasses import dataclass, fields

from huaytools.utils.dataclass_utils import DataclassUtils


class BunchDict(dict):
    """
    基于 dict 实现 Bunch 模式

    实现方法：
        - 通过重写 __getattr__、__setattr__、__delattr__ 同步 o.x 和 o['x'] 的行为
        - 为了防止与内部成员冲突，比如 __dict__，会预先调用 __getattribute__（优先级高于 __getattr__）

    Notes:
        - [2022.08.25] 通过对 __dict__ 添加 property 装饰限制修改，防止以下行为：
            - 如果直接向 __dict__ 添加属性，且存在同名 key，将导致 o.key 和 o['key'] 不一致；
            - 示例：
                ```python
                o = BunchDict(a=1, b=2)
                o.__dict__['a'] = 10
                print(o.a, o['a'])  # 10, 1
                ```

    Examples:
        >>> x = BunchDict(a=1, b=2)
        >>> x
        {'a': 1, 'b': 2}
        >>> x.c = 3  # x['c'] = 3
        >>> 'c' in x
        True
        >>> x['c']
        3
        >>> x['d'] = {'bar': 6}  # x.d = {'bar': 6}
        >>> hasattr(x, 'd')
        True
        >>> x.d.bar
        6
        >>> dir(x)
        ['a', 'b', 'c', 'd']
        >>> vars(x)
        {'a': 1, 'b': 2, 'c': 3, 'd': {'bar': 6}}
        >>> del x.a
        >>> x.a
        Traceback (most recent call last):
            ...
        AttributeError: a
        >>> x.__dict__
        {'b': 2, 'c': 3, 'd': {'bar': 6}}
        >>> x.__dict__ = {'a': 123}  # noqa
        Traceback (most recent call last):
            ...
        AttributeError: can't set attribute

        >>> y = {'foo': {'a': 1, 'bar': {'c': 'C'}}, 'b': 2}
        >>> y == BunchDict.from_dict(y) == BunchDict(y)
        True
        >>> x = BunchDict(y, d={'z': 26})
        >>> x.foo
        {'a': 1, 'bar': {'c': 'C'}}
        >>> x.foo.bar
        {'c': 'C'}
        >>> all(type(it) == BunchDict for it in [x.foo, x.foo.bar, x.d])  # noqa
        True

    References:
        - bunch（pip install bunch）
    """

    # __slots__ = ()
    __dict__ = property(lambda self: self)
    """ 禁止修改 __dict__ """

    def __dir__(self):
        """ 屏蔽其他属性或方法 """
        return self.keys()

    def __init__(self, seq: Union[Mapping, Iterable] = None, **kwargs):
        """"""
        super().__init__()  # 初始化 self，一个空 dict

        # 模拟向 dict 中添加元素的过程：https://docs.python.org/zh-cn/3/library/stdtypes.html#mapping-types-dict
        #   通过手动添加元素，确保每个类型为 dict 的值会被初始化为 BunchDict
        if seq is not None:
            if isinstance(seq, Mapping):
                seq = seq.items()
            for k, v in seq:
                self[k] = BunchDict.bunching(v)  # 如果 v 的类型为 dict，将被修改为 BunchDict

        for k, v in kwargs.items():
            self[k] = BunchDict.bunching(v)

    def __getattr__(self, name: str):
        """ 使 `o.name` 等价于 `o[name]` """
        try:
            # 除非是来自 object 或 dict 的特殊属性，比如 __doc__ 等
            return super().__getattribute__(name)
        except AttributeError:
            try:
                return self[name]
            except KeyError:
                raise AttributeError(name)

    def __setattr__(self, name: str, value):
        """ 使 `o.name = value` 等价于 `o[name] = value` """
        try:
            # 除非是来自 object 或 dict 的特殊属性，比如 __doc__ 等
            super().__getattribute__(name)
        except AttributeError:
            self[name] = value
        else:
            # setattr(self, name, value)  # RecursionError
            super().__setattr__(name, BunchDict.bunching(value))

    def __delattr__(self, name: str):
        """ 使 `del o.name` 等价于 `del o[name]` """
        try:
            # 除非是来自 object 或 dict 的特殊属性，比如 __doc__ 等
            super().__getattribute__(name)
        except AttributeError:
            try:
                del self[name]
            except KeyError:
                raise AttributeError(name)
        else:
            super().__delattr__(name)

    def __setitem__(self, key: str, value):
        """ 添加新元素，对 value 进行 bunching """
        super().__setitem__(key, BunchDict.bunching(value))

    @staticmethod
    def bunching(x: Union[Mapping, Any]) -> Union['BunchDict', Any]:
        return _bunching(x)

    @classmethod
    def from_dict(cls, d: dict) -> 'BunchDict':
        """ create from dict """
        return cls.bunching(d)

    def to_dict(self) -> dict:
        return _unbunch(self)


def _bunching(x) -> Union[BunchDict, Any]:
    """
    Recursively transforms a dictionary into a Bunch.

    Examples:
        >>> b = _bunching({'urmom': {'sez': {'what': 'what'}}})
        >>> b.urmom.sez.what
        'what'
        >>> b = _bunching({ 'lol': ('cats', {'hah':'i win'}), 'hello': [{'french':'salut', 'german':'hallo'}]})
        >>> b.hello[0].french
        'salut'
        >>> b.lol[1].hah
        'i win'
    """
    if isinstance(x, Mapping):
        return BunchDict((k, _bunching(v)) for k, v in x.items())
    elif isinstance(x, (list, tuple)):
        return type(x)(_bunching(v) for v in x)
    else:
        return x


def _unbunch(x: BunchDict) -> dict:
    """
    Recursively converts a Bunch into a dictionary.

    Examples:

        >>> b = BunchDict(foo=BunchDict(lol=True), hello=42, ponies='are pretty!')
        >>> _unbunch(b)
        {'foo': {'lol': True}, 'hello': 42, 'ponies': 'are pretty!'}

        unbunchify will handle intermediary dicts, lists and tuples (as well as
        their subclasses), but ymmv on custom datatypes.

        >>> b = BunchDict(foo=['bar', BunchDict(lol=True)], hello=42, ponies=('pretty!', BunchDict(lies='trouble!')))
        >>> _unbunch(b)
        {'foo': ['bar', {'lol': True}], 'hello': 42, 'ponies': ('pretty!', {'lies': 'trouble!'})}

        nb. As dicts are not hashable, they cannot be nested in sets/frozensets.
    """
    if isinstance(x, BunchDict):
        return dict((k, _unbunch(v)) for k, v in x.items())
    elif isinstance(x, (list, tuple)):
        return type(x)(_unbunch(v) for v in x)
    else:
        return x


@dataclass
class DataclassDict(dict):
    """
    Dataclass 字典：将 field 默认保存到一个字典中

    Examples:
        >>> from dataclasses import field
        >>> @dataclass
        ... class Features(DataclassDict):
        ...     a: int = 1
        ...     b: str = 'B'
        ...     c: list = field(default_factory=list)
        >>> f = Features(); f
        Features(a=1, b='B', c=[])
        >>> f.a = 2; f['a']
        2
        >>> f['a'] = 3; f.a
        3
        >>> f['d'] = 'D'
        >>> f.d  # noqa
        Traceback (most recent call last):
            ...
        AttributeError: 'Features' object has no attribute 'd'
        >>> not hasattr(f, 'd') and 'd' in f
        True
        >>> DataclassUtils.get_field_names(f)
        ['a', 'b', 'c']
        >>> f.c.append('Foo')
        >>> import json
        >>> json.dumps(f)  # 可以直接当做 dict 处理
        '{"a": 3, "b": "B", "c": ["Foo"], "d": "D"}'
    """

    def __post_init__(self):
        """"""
        # 把 field 依次添加到 dict 中
        for f in fields(self):
            self[f.name] = getattr(self, f.name)

    def __setattr__(self, key, value):
        """"""
        super().__setattr__(key, value)
        if key in DataclassUtils.get_field_names(self):
            super().__setitem__(key, value)

        # if key in DataclassUtils.get_field_names(self):
        #     super().__setattr__(key, value)
        #     super().__setitem__(key, value)
        # else:
        #     # raise KeyError(key)
        #     # 禁止添加新属性，除非是修改魔术属性
        #     try:
        #         super().__getattribute__(key)
        #     except AttributeError:
        #         raise KeyError(key)
        #     else:
        #         super().__setattr__(key, value)

    def __setitem__(self, key, value):
        """"""
        super().__setitem__(key, value)
        if key in DataclassUtils.get_field_names(self):
            super().__setattr__(key, value)

        # if key in DataclassUtils.get_field_names(self):
        #     super().__setitem__(key, value)
        #     super().__setattr__(key, value)
        # else:
        #     raise KeyError(key)

    # def __str__(self):
    #     return dict.__str__(self)
