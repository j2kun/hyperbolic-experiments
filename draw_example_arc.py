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


if __name__ == '__main__':
    run('basic_shapes.svg')
