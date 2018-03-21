"""
Module with generally used tools
"""
from collections import Counter

DEBUG = True


def debug(*args):
    if DEBUG:
        print(*args)


def compare(s: "List", t: "List"):
    return Counter(s) == Counter(t)
