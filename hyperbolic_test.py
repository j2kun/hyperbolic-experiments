from hyperbolic import *


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

    norm = ((actual_inverse[0] - expected_inverse[0]) ** 2
            + (actual_inverse[1] - expected_inverse[1]) ** 2)
    assert abs(norm) < 1e-8


def test_circle_through_points_normal():
    pass


def test_circle_through_points_diameter():
    pass
