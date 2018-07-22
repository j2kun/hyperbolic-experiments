import math

from hyperbolic import *


def assertAreClose(v1, v2):
    norm = sum((x1 - x2) ** 2 for (x1, x2) in zip(v1, v1))
    assert norm ** 0.5 < EPSILON


def test_invert_in_circle_horizontal():
    center = (1, 1)
    radius = 5
    point = (4, 1)
    expected_inverse = (1 + 25 / 3, 1)

    assert expected_inverse == invert_in_circle(
            Circle(center, radius), point)


def test_invert_in_circle_diagonal():
    center = (0, 0)
    radius = 2 ** 0.5
    point = (2, 2)
    expected_inverse = (1/2, 1/2)
    actual_inverse = invert_in_circle(Circle(center, radius), point)
    assertAreClose(actual_inverse, expected_inverse)


def test_circle_through_points_unit_circle():
    reference_circle = Circle((0, 0), 1)
    p1 = (1/2, 1/2)
    p2 = (1/2, -1/2)

    expected_circle = Circle((3/2, 0), (5/4) ** 0.5)
    assert expected_circle == circle_through_points_perpendicular_to_circle(p1, p2, reference_circle)


def test_circle_through_points_diameter():
    reference_circle = Circle((0, 0), 1)
    p1 = (1/3, 1/4)
    p2 = (-1/3, -1/4)

    try:
        circle_through_points_perpendicular_to_circle(p1, p2, reference_circle)
        assert False
    except:
        pass


def test_rotate_around_origin_pi_over_3():
    angle = math.pi / 3
    assertAreClose((1 / 2, 3 ** 0.5 / 2), rotate_around_origin(angle, (1, 0)))
    assertAreClose((-3 ** 0.5 / 2, 1/2), rotate_around_origin(angle, (0, 1)))
