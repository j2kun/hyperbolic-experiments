from assertpy import assert_that
from geometry import Point
from geometry import rotate_around_origin
import itertools
import math

from tessellation import *
from testing import *


def test_valid_configuration():
    TessellationConfiguration(6, 4)
    TessellationConfiguration(4, 5)
    TessellationConfiguration(7, 3)
    TessellationConfiguration(3, 7)


def test_invalid_configuration():
    try:
        TessellationConfiguration(4, 4)
        assert False
    except Exception:
        pass


def test_center_polygon():
    config = TessellationConfiguration(6, 4)
    tessellation = HyperbolicTessellation(config)

    starting_vertex = Point(x=0.44828773608, y=0.258819045102)
    vertices = [
        rotate_around_origin(k * math.pi / 6, starting_vertex)
        for k in range(6)
    ]

    assert_iterables_are_close(tessellation.compute_center_polygon(), vertices)
