from assertpy import assert_that
import math
import pytest

from geometry import *


def assertAreClose(v1, v2):
    norm = sum((x1 - x2) ** 2 for (x1, x2) in zip(v1, v1))
    assert_that(norm ** 0.5).is_less_than(EPSILON)


def test_line_y_value():
    line = Line(Point(2, 3), slope=4)
    assert_that(line.y_value(x_value=4)).is_equal_to(11)


def test_vertical_line_y_value():
    line = VerticalLine.at_point(Point(2, 3))
    with pytest.raises(TypeError):
        line.y_value(x_value=4)


def test_line_eq():
    line1 = Line(Point(1, 0), slope=2)
    line2 = Line(Point(2, 2), slope=2)
    assert_that(line1 == line2).is_true()
    assert_that(line2 == line1).is_true()


def test_line_neq():
    line1 = Line(Point(1, 0), slope=2)
    line2 = Line(Point(0, -2), slope=2.1)
    assert_that(line1 != line2).is_true()
    assert_that(line2 != line1).is_true()


def test_vertical_line_eq():
    line1 = VerticalLine.at_point(Point(2, 5))
    line2 = VerticalLine.at_point(Point(2, -1))
    assert_that(line1 == line2).is_true()
    assert_that(line2 == line1).is_true()


def test_vertical_line_neq():
    line1 = VerticalLine.at_point(Point(2, 5))
    line2 = VerticalLine.at_point(Point(2.1, -1))
    assert_that(line1 != line2).is_true()
    assert_that(line2 != line1).is_true()


def test_vertical_line_neq_line():
    line1 = VerticalLine.at_point(Point(2, 5))
    line2 = Line(Point(2, 5), slope=1)
    assert_that(line1 != line2).is_true()
    assert_that(line2 != line1).is_true()


def test_line_intersect_with():
    line1 = Line(Point(4, 3), slope=2)
    line2 = Line(Point(-2, -1), slope=1)
    assert_that(line1.intersect_with(line2)).is_equal_to(Point(6, 7))
    assert_that(line2.intersect_with(line1)).is_equal_to(Point(6, 7))


def test_line_intersect_with_both_horizontal():
    line1 = Line(Point(4, 3), slope=0)
    line2 = Line(Point(-2, -1), slope=0)
    with pytest.raises(ValueError):
        line1.intersect_with(line2)


def test_line_intersect_with_self():
    line1 = Line(Point(4, 3), slope=0)
    with pytest.raises(ValueError):
        line1.intersect_with(line1)


def test_vertical_line_intersect_with():
    line1 = VerticalLine.at_point(Point(4, -10))
    line2 = Line(Point(-2, -1), slope=1)
    assert_that(line1.intersect_with(line2)).is_equal_to(Point(4, 5))
    assert_that(line2.intersect_with(line1)).is_equal_to(Point(4, 5))


def test_vertical_line_intersect_with_vertical_line():
    line1 = VerticalLine.at_point(Point(4, -10))
    line2 = VerticalLine.at_point(Point(5, 2))
    with pytest.raises(ValueError):
        line1.intersect_with(line2)


def test_vertical_line_intersect_with_self():
    line1 = Line(Point(4, 3), slope=0)
    with pytest.raises(ValueError):
        line1.intersect_with(line1)


def test_circle_contains():
    circle = Circle(center=Point(0, 0), radius=1)
    points = [
        Point(1, 0),
        Point(0, 1),
        Point(math.cos(2 * math.pi / 5), math.sin(2 * math.pi / 5)),
    ]
    for point in points:
        assert_that(circle.contains(point)).is_true()


def test_tangent_at_point_not_on_circle():
    circle = Circle(center=Point(0, 0), radius=1)
    point = Point(0, 2)
    with pytest.raises(ValueError):
        circle.tangent_at(point)


def test_tangent_at_produces_vertical_line():
    circle = Circle(center=Point(0, 0), radius=1)
    point = Point(1, 0)
    expected_line = VerticalLine.at_point(point)
    assert_that(circle.tangent_at(point)).is_equal_to(expected_line)


def test_tangent_at_simple():
    circle = Circle(center=Point(0, 0), radius=1)
    point = Point(0, 1)
    expected_line = Line(point=point, slope=0)
    assert_that(circle.tangent_at(point)).is_equal_to(expected_line)


def test_tangent_at_angled():
    circle = Circle(center=Point(1, 2), radius=2)
    sqrt3 = math.sqrt(3)
    point = Point(2, 2 + sqrt3)
    expected_line = Line(point=point, slope=-1/sqrt3)
    assert_that(circle.tangent_at(point)).is_equal_to(expected_line)


def test_invert_in_circle_horizontal():
    circle = Circle(center=Point(1, 1), radius=5)
    point = Point(4, 1)
    expected_inverse = Point(1 + 25 / 3, 1)
    assert_that(circle.invert_point(point)).is_equal_to(expected_inverse)


def test_invert_in_circle_diagonal():
    circle = Circle(center=Point(0 , 0), radius=2 ** 0.5)
    point = (2, 2)
    expected_inverse = (1/2, 1/2)
    actual_inverse = circle.invert_point(point)
    assertAreClose(actual_inverse, expected_inverse)


def test_circle_through_points_unit_circle():
    reference_circle = Circle(Point(0, 0), 1)
    p1 = Point(1/2, 1/2)
    p2 = Point(1/2, -1/2)

    expected_circle = Circle(Point(3/2, 0), (5/4) ** 0.5)
    actual_circle = circle_through_points_perpendicular_to_circle(p1, p2, reference_circle)
    assert_that(expected_circle).is_equal_to(actual_circle)


def test_circle_through_points_diameter():
    reference_circle = Circle(Point(0, 0), 1)
    p1 = Point(1/3, 1/4)
    p2 = Point(-1/3, -1/4)

    with pytest.raises(ValueError):
        circle_through_points_perpendicular_to_circle(p1, p2, reference_circle)


def test_rotate_around_origin_pi_over_3():
    angle = math.pi / 3
    assertAreClose((1 / 2, 3 ** 0.5 / 2), rotate_around_origin(angle, (1, 0)))
    assertAreClose((-3 ** 0.5 / 2, 1/2), rotate_around_origin(angle, (0, 1)))
