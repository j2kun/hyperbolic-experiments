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


def render(p):
    if isinstance(p, tuple):
        (x, y) = p
        return translate(scale((x, -y)))
    else:
        return scale(p)


def run(name):
    """Draw some basic arcs of cricles perpendicular to a reference circle.
    """
    dwg = svgwrite.Drawing(filename=name, debug=True)
    dwg.fill(color='white', opacity=0)

    reference_circle = Circle((0,0), 1)
    reference_circle = Circle(render(reference_circle.center), render(reference_circle.radius))

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

    reference_circle = Circle(Point(0, 0), radius=1)
    boundary_circle = dwg.circle(
        center=render(reference_circle.center),
        r=render(reference_circle.radius),
        id='boundary_circle',
        stroke='black',
        stroke_width=1)
    boundary_circle.fill(color='white', opacity=0)
    dwg.add(boundary_circle)

    triangle = dwg.add(dwg.g(id='triangle', stroke='red', stroke_width=4))


    for n in range(5, 11):
        z = math.cos(math.pi / n) ** 2 / math.sin(math.pi / n)
        y1 = -1 / z
        y2 = 1 / z
        print((n, z, y1))
        x = math.sqrt(1 - y1**2)

        p1 = Point(x, y1)
        p2 = Point(x, y2)

        fundamental_triangle_side = circle_through_points_perpendicular_to_circle(
                p1, p2, reference_circle)

        # draw two diameters for the easy edges.
        triangle.add(
                dwg.line(render((0, 0)), render((1, 0))))
        triangle.add(
                dwg.line(
                    render((0, 0)),
                    render((math.cos(math.pi / n), math.sin(math.pi / n)))))

        draw_arc(dwg, triangle, p1, p2, fundamental_triangle_side.radius,
                fundamental_triangle_side.center, id="triangle_side_n_{}".format(n))

    dwg.save()


def draw_and_rotate_fundamental_triangle_around_center(name):
    """A test to verify a formula related to the fundamental triangle.

    If we reflect it, does it wrap all the way around?
    """
    dwg = svgwrite.Drawing(filename=name, debug=True)
    dwg.fill(color='white', opacity=0)

    reference_circle = Circle(Point(0, 0), radius=1)
    boundary_circle = dwg.circle(
        center=render(reference_circle.center),
        r=render(reference_circle.radius),
        id='boundary_circle',
        stroke='black',
        stroke_width=1)
    boundary_circle.fill(color='white', opacity=0)
    dwg.add(boundary_circle)

    triangle = dwg.add(dwg.g(id='rotated_triangle', stroke='red', stroke_width=4))

    n = 6
    z = math.cos(math.pi / n) ** 2 / math.sin(math.pi / n)
    y1 = -1 / z
    y2 = 1 / z
    x = math.sqrt(1 - y1**2)

    p0 = Point(0, 0)
    # these are ideal points
    ideal1 = Point(x, y1)
    ideal2 = Point(x, y2)

    """We need to intersect the circle defined by the ideal points (ideal1, ideal2)
    with the lines [(0, 0), (cos(pi/n), sin(pi/n))] and [(0, 0), (1, 0)].
    """
    triangle_side = circle_through_points_perpendicular_to_circle(
            ideal1, ideal2, reference_circle)

    top_intersection_points = triangle_side.intersect_with_line(
            Line(Point(0, 0), math.sin(math.pi / n) / math.cos(math.pi / n)))

    p1 = min(top_intersection_points, key=lambda p: distance(p0, p))

    bottom_intersection_points = triangle_side.intersect_with_line(
            Line(Point(0, 0), 0))

    p2 = min(bottom_intersection_points, key=lambda p: distance(p0, p))

    for i in range(n):
        draw_triangle(dwg, triangle, p0, p1, p2, reference_circle)
        p0, p1, p2 = reflect([p0, p1, p2], 0, 1, reference_circle.center)
        draw_triangle(dwg, triangle, p0, p1, p2, reference_circle)
        p0, p1, p2 = reflect([p0, p1, p2], 0, 2, reference_circle.center)

    dwg.save()


def draw_and_rotate_fundamental_triangle_around_vertex(name):
    """A test to verify a formula related to the fundamental triangle.

    If we reflect it, does it wrap all the way around?
    """
    dwg = svgwrite.Drawing(filename=name, debug=True)
    dwg.fill(color='white', opacity=0)

    reference_circle = Circle(Point(0, 0), radius=1)
    boundary_circle = dwg.circle(
        center=render(reference_circle.center),
        r=render(reference_circle.radius),
        id='boundary_circle',
        stroke='black',
        stroke_width=1)
    boundary_circle.fill(color='white', opacity=0)
    dwg.add(boundary_circle)

    triangle = dwg.add(dwg.g(id='rotated_triangle', stroke='red', stroke_width=4))

    p = 6
    q = 4
    center, top, bottom = compute_fundamental_triangle(p, q)

    p0, p1, p2 = center, top, bottom
    for i in range(q):
        draw_triangle(dwg, triangle, p0, p1, p2, reference_circle)
        p0, p1, p2 = reflect([p0, p1, p2], 0, 1, reference_circle)
        draw_triangle(dwg, triangle, p0, p1, p2, reference_circle)
        p0, p1, p2 = reflect([p0, p1, p2], 1, 2, reference_circle)

    p0, p1, p2 = center, top, bottom
    for i in range(p):
        draw_triangle(dwg, triangle, p0, p1, p2, reference_circle)
        p0, p1, p2 = reflect([p0, p1, p2], 0, 1, reference_circle)
        draw_triangle(dwg, triangle, p0, p1, p2, reference_circle)
        p0, p1, p2 = reflect([p0, p1, p2], 0, 2, reference_circle)

    dwg.save()


def reflect(points, index1, index2, reference_circle):
    p, q = points[index1], points[index2]
    print("\nReflecting \n {} \nacross the line \n {}".format(
        points, [p, q]))

    if orientation(p, q, reference_circle.center) == 'collinear':
        # reflect across diameter spanning p -> q
        reflection_line = Line.through(p, q)
        return tuple(reflection_line.reflect(p) for p in points)
    else:
        fundamental_triangle_side = circle_through_points_perpendicular_to_circle(
                p, q, reference_circle)
        output = tuple(
            fundamental_triangle_side.invert_point(p) for p in points
        )
        print("reflected is {}".format(output))
        return tuple(
            fundamental_triangle_side.invert_point(p) for p in points
        )


def draw_triangle(dwg, triangle, p1, p2, p3, disk_boundary):
    print("\nDrawing triangle \n {}\n {}\n {}".format(p1, p2, p3))
    # for each pair, draw straight line if diameter, otherwise draw arc
    for (p, q) in [(p1, p2), (p2, p3), (p1, p3)]:
        if orientation(p, q, disk_boundary.center) == 'collinear':
            line = dwg.line(render(p), render(q))
            triangle.add(line)
        else:
            hyperbolic_line = circle_through_points_perpendicular_to_circle(
                p, q, disk_boundary)

            draw_arc(dwg, triangle, p, q,
                    hyperbolic_line.radius,
                    hyperbolic_line.center)


def draw_arc(dwg, lines, p1, p2, r, circle_center, id=None):
    use_positive_angle_dir = orientation(p1, p2, circle_center) == 'clockwise'

    """
    Claim: Let x, y, be the start and end of the hyperbolic line segment,
    and c the center of the circle this line segment is a part of. Then we
    should use angle_dir='+' if and only if the sequence (x, y, c) makes a
    clockwise turn. Note this is in the coordinates with a flipped y-axis from
    the standard coordinates.
    """

    p1 = render(p1)
    p2 = render(p2)
    r = render(r)
    circle_center = render(circle_center)

    if id:
        path = dwg.path('m', id=id)
    else:
        path = dwg.path('m')

    path.push(p1)
    path.push_arc(
        target=p2,
        rotation=0,
        r=r,
        large_arc=False,
        angle_dir='+' if use_positive_angle_dir else '-',
        absolute=True)

    """ Uncomment to see the circle containing this arc
    dwg.add(dwg.circle(
        center=circle_center,
        r=r,
        stroke='green',
        stroke_width=1))
    """

    lines.add(path)


def compute_fundamental_triangle(p, q):
    center = Point(0, 0)
    cos_p, sin_p = math.cos(math.pi / p), math.sin(math.pi / p)

    """Desired point is b = (b_x, b_y). This point is on the line
    y = (sin_p / cos_p) x and on an unknown circle C perpendicular to the unit
    circle with center g = (g_x, 0).

    If a = (0, 0) and d = (d_x, 0) is the intersection of the line [ag] with C,
    then we need (hyperbolic) angle abd to be pi / q.

    This is the same as requiring that the tangent line to C at b forms an angle
    of pi / q with the line between a and (cos_p, sin_p).

    This tangent line has equation

        y - b_y = m_b (x - b_x)    where m_b = -(b_x - g_x) / b_y

    from the point b, the line is represented by the vector (1, m_b), and translating
    that to the center (imagining) we see that the sum of angle dab and
    (hyperbolic) angle abd is pi / p + pi / q, giving

        tan(pi / p + pi / q) = -m_b

    Or equivalently, using the fact that b is on y = (sin_p / cos_p) x,

        tan(pi / p + pi / q) (sin_p / cos_p) = (G_x - b_x) / b_x
    """

    g_x = math.sqrt(2)
    Z = math.tan(math.pi / p + math.pi / q) * sin_p / cos_p
    b_x = g_x / (Z + 1)

    b_y = b_x * (sin_p / cos_p)
    b = Point(b_x, b_y)

    d_x = g_x - math.sqrt(b_y ** 2 + (b_x - g_x) ** 2)

    return [center, b, Point(d_x, 0)]



if __name__ == '__main__':
    draw_and_rotate_fundamental_triangle_around_vertex('rotated_triangle_vertex.svg')
