from assertpy import assert_that
from geometry import Point
import itertools
import math

from tessellation import *
from testing import *


def test_fundamental_triangle():
    config = TessellationConfiguration(6, 4)
    center, pi_over_q_vertex, x_axis_vertex = compute_fundamental_triangle(config)
    assert_that(center).is_equal_to(Point(0, 0))
    assert_iterables_are_close(x_axis_vertex, Point(math.sqrt(2) - 1, 0))

    b_x = 0.5 * math.sqrt(6 - 3 * math.sqrt(3))
    b_y = 0.5 * math.sqrt(2 - math.sqrt(3))
    assert_iterables_are_close(pi_over_q_vertex, Point(x=b_x, y=b_y))
