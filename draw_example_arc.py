from svgwrite import cm, mm
import math
import svgwrite

from geometry import *


width = 800
height = 800

# translate so that center is (400, 400) and unit radius is 100
scaling = 250
translation = (400, 400)


def scale(p):
    if isinstance(p, tuple):
        return tuple(scaling * x for x in p)
    else:
        return scaling * p


def translate(p):
    return [x + dx for (x, dx) in zip(p, translation)]


def run(name):
    """Draw some basic arcs of cricles perpendicular to a reference circle.
    """
    dwg = svgwrite.Drawing(filename=name, debug=True)
    dwg.fill(color='white', opacity=0)

    reference_circle = Circle((0,0), 1)
    reference_circle = Circle(translate(scale(reference_circle.center)), scale(reference_circle.radius))

    boundary_circle = dwg.circle(
        center=reference_circle.center,
        r=reference_circle.radius,
        id='boundary_circle',
        stroke='black',
        stroke_width=1)
    boundary_circle.fill(color='white', opacity=0)
    dwg.add(boundary_circle)

    lines = dwg.add(dwg.g(id='lines', stroke='red', stroke_width=4))

    p1 = (1/2, 1/2)
    p2 = (1/2, -1/2)
    r = (5/4) ** 0.5
    circle_center = (3/2, 0)

    N = 32
    degrees = 2 * math.pi / N

    for i in range(N):
        draw_arc(dwg, lines, p1, p2, r, circle_center, id=i)
        p1 = rotate_around_origin(degrees, p1)
        p2 = rotate_around_origin(degrees, p2)
        circle_center = rotate_around_origin(degrees, circle_center)

    dwg.save()


def draw_fundamental_triangle(name):
    """A test to verify a formula related to the fundamental triangle."""
    dwg = svgwrite.Drawing(filename=name, debug=True)
    dwg.fill(color='white', opacity=0)

    reference_circle = Circle((0,0), 1)
    n = 6
    z = math.cos(math.pi / 6) ** 2 / math.sin(math.pi / 6)
    y1 = 1 / z
    y2 = -1 / z
    x = math.sqrt(1 - y1**2)

    p1 = (x, y1)
    p2 = (x, y2)

    fundamental_triangle_side = circle_through_points_perpendicular_to_circle(
            p1, p2, reference_circle)

    boundary_circle = dwg.circle(
        center=translate(scale(reference_circle.center)),
        r=scale(reference_circle.radius),
        id='boundary_circle',
        stroke='black',
        stroke_width=1)
    boundary_circle.fill(color='white', opacity=0)
    dwg.add(boundary_circle)

    triangle = dwg.add(dwg.g(id='triangle', stroke='red', stroke_width=4))

    # draw two diameters for the easy edges.
    triangle.add(
            dwg.line(translate(scale((0, 0))), translate(scale((1, 0)))))
    triangle.add(
            dwg.line(
                translate(scale((0, 0))),
                translate(scale((math.cos(math.pi / n), math.sin(math.pi / n))))))

    draw_arc(dwg, triangles, p1, p2, fundamental_triangle_side.radius,
            fundamental_triangle_side.center)
    dwg.save()


def draw_arc(dwg, lines, p1, p2, r, circle_center, id):
    use_positive_angle_dir = orientation(p1, p2, circle_center) == 'counterclockwise'

    """
    Hypothesis: Let x, y, be the start and end of the hyperbolic line segment,
    and c the center of the circle this line segment is a part of. Then we
    should use angle_dir='+' if and only if the sequence (x, y, c) makes a
    counterclockwise turn.
    """

    p1 = translate(scale(p1))
    p2 = translate(scale(p2))
    r = scale(r)
    circle_center = translate(scale(circle_center))

    path = dwg.path('m', id=str(id) + '_' + orientation(p1, p2, circle_center))
    path.push(p1)
    path.push_arc(
        target=p2,
        rotation=0,
        r=r,
        large_arc=False,
        angle_dir='+' if use_positive_angle_dir else '-',
        absolute=True)

    dwg.add(dwg.circle(
        center=circle_center,
        r=r,
        stroke='green',
        stroke_width=1))

    lines.add(path)


def bleh():
    num_sides = 6  # number of sides of the resulting polygon
    num_per_vertex = 5  # number of polygons at each vertex

    # make the fundamental right triangle with angle measures
    # pi / p, pi / q, and pi
    # the pi / p angle is at the center
    center = (0, 0)
    bottom_edge_ideal_point = (1, 0)
    top_edge_ideal_point = (cos(pi / num_sides), sin(pi / num_sides))

    """Let C be the center of the circle.

    Let X be a point along the line [C, top_edge_ideal_point].

    For any choice of X, there is a corresponding choice of Y on the line [C,
    (0,1)] for which [C, X] and [C, Y] make a right angle.

    I want the C chosen so that the angle between [C, X] and [X, Y] is pi / q.
    """


if __name__ == '__main__':
    draw_fundamental_triangle('fundamental_triangle.svg')
