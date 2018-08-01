from assertpy import assert_that
from geometry import EPSILON


def is_close(v1, v2):
    try:
        return v1.is_close_to(v2)
    except AttributeError:
        return abs(v1 - v2) < EPSILON


def assert_are_close(v1, v2):
    assert_that(is_close(v1, v2)).is_true()


def assert_iterables_are_close(s1, s2):
    # two iterables are close if each item in one is close to some item
    # in the other
    for item in s1:
        assert_that(any(is_close(item, x) for x in s2)).is_true()

    for item in s2:
        assert_that(any(is_close(item, x) for x in s1)).is_true()

