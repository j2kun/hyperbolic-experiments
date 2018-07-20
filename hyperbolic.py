"""Geometry functions related to hyperbolic geometry."""

from collections import namedtuple


EPSILON = 1e-8
Circle = namedtuple('Circle', ['center', 'radius'])


def invert_in_circle(circle, point):
    """Compute the inverse of a point with respect to a circle."""
    x, y = point
    (center_x, center_y), radius = circle
    square_norm = (x - center_x) ** 2 + (y - center_y) ** 2
    x_inverted = center_x + radius ** 2 * (x - center_x) / square_norm
    y_inverted = center_y + radius ** 2 * (y - center_y) / square_norm
    return (x_inverted, y_inverted)


def det3(A):
    """Compute the determinant of a 3x3 matrix"""
    if not (len(A) == 3 and len(A[0]) == 3):
        raise Exception("Bad matrix dims")

    return (
        A[0][0] * (A[1][1] * A[2][2] - A[1][2] * A[2][1])
      - A[0][1] * (A[1][0] * A[2][2] - A[1][2] * A[2][0])
      + A[0][2] * (A[1][0] * A[2][1] - A[1][1] * A[2][0])
    )


def remove_column(A, removed_col_index):
    return [
        [entry for j, entry in enumerate(row) if j != removed_col_index]
        for row in A
    ]


def circle_through_points_perpendicular_to_circle(point1, point2, circle):
    """Return a Circle that passes through the two given points and
    intersects the given circle at a perpendicular angle.

    A hyperbolic line between two points is computed as the circle arc
    perpendicular to the boundary circle that passes between those points.
    This can be constructed by first inverting one of the points in the
    circle, then constructing the circle passing through all three points.

    Note, if the two points and the center of the input circle lie on a
    common line, then the hyperbolic line is a diameter of the circle. This
    function assumes that case has been checked in advance, with an Exception
    raised otherwise.
    """
    point3 = invert_in_circle(circle, point1)

    def row(point):
        (x, y) = point
        return [x ** 2 + y ** 2, x, y, 1]

    # The equation for the center of the circle passing through three points
    # is given by the determinants of a cleverly chosen matrix.
    M = [
        row(point1),
        row(point2),
        row(point3),
    ]

    detminor_1_1 = det3(remove_column(M, 0))
    if abs(detminor_1_1) < EPSILON:
        raise Exception("input points {} {} lie on a line with the "
            "center of the circle {}".format(point1, point2, circle))

    # detminor stands for "determinant of (matrix) minor"
    detminor_1_2 = det3(remove_column(M, 1))
    detminor_1_3 = det3(remove_column(M, 2))
    detminor_1_4 = det3(remove_column(M, 3))

    circle_center_x = 0.5 * detminor_1_2 / detminor_1_1
    circle_center_y = -0.5 * detminor_1_3 / detminor_1_1
    circle_radius = (
        circle_center_x ** 2
      + circle_center_y ** 2
      + detminor_1_4 / detminor_1_1
    ) ** 0.5

    return Circle((circle_center_x, circle_center_y), circle_radius)


def rotate_around_origin(angle, point):
    """Rotate the given point about the origin by the given angle."""
    pass
