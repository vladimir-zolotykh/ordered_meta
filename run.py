#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from collections import OrderedDict


class Typed:
    expected_type = type(None)

    def __init__(self, name=None):
        self._name = name

    def __set__(self, instance, value):
        if not isinstance(value, self.expected_type):
            raise TypeError("Expected {!r}".format(self.expected_type.__name__))
        instance.__dict__[self._name] = value


class Integer(Typed):
    expected_type = int


class Float(Typed):
    expected_type = float


class String(Typed):
    expected_type = str


class OrderedMeta(type):
    def __new__(cls, clsname, bases, clsdict):
        d = dict(clsdict)
        _order = []
        for name, value in clsdict.items():
            if isinstance(value, Typed):
                value._name = name
                _order.append(name)
        d["_order"] = _order
        return super().__new__(cls, clsname, bases, d)

    @classmethod
    def __prepare__(mcls, name, bases, **kwars):
        return OrderedDict()


class OrderedStruct(metaclass=OrderedMeta):
    def as_csv(self):
        return ",".join(name for name in self._order)


class Stock(OrderedStruct):
    name = String()
    shares = Integer()
    price = Float()

    def __init__(self, name, shares, price):
        self.name = name
        self.shares = shares
        self.price = price


if __name__ == "__main__":
    stock = Stock("GOOG", 100, 490.1)
    print(stock.name)
    print(stock.as_csv())
    try:
        stock = Stock("AAPL", "a lot", 610.23)
    except TypeError as e:
        print(e)
