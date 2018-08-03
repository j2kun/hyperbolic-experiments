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
    assert_iterables_are_close(pi_over_q_vertex, Point(x=0.44828773608402694, y=0.2588190451025208))
