#!/usr/bin/env python3

result = []


def get_subclasses_exception():
    classtree(Exception)
    return result


def classtree(cls):
    result.append(cls.__name__)
    for subcls in cls.__subclasses__():
        classtree(subcls)
