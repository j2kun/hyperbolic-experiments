from math import sin, cos, pi
import geometry


def compute_fundamental_triangle(p, q):
    """Compute the vertices of the hyperbolic triangle with the following
    properties:

     - Vertex A lies at the origin.
     - Vertex C lies on the x-axis.
     - Vertex B is chosen so that angle CAB is pi / p, and (hyperbolic) angle
       ABC is pi / q.

    Derivation:

    The desired point is B = (b_x, b_y). This point is on the line
    L: y = tan(pi / p) x and on an unknown circle C perpendicular to the unit
    circle with center G = (g_x, 0).

    If A = (0, 0) and D = (d_x, 0) is the intersection of the line [AG] with C,
    then we need (hyperbolic) angle ABD to be pi / q. This is the same as
    requiring that the tangent line to C at B forms an angle of pi / q with the
    line between A and (cos(pi / q), sin(pi / q)), which has slope
    tan(pi / p + pi / q).

    The slope of a tangent line to circle C at point B is given by

        y'(B) = -(b_x - g_x) / b_y

    Setting y'(B) = tan(pi / p + pi / q) and writing b_y in terms of b_x gives

        tan(pi / p + pi / q) tan(pi / p) = (G_x - b_x) / b_x

    Or, letting Z = tan(pi / p + pi / q) tan(pi / p),

        b_x(Z + 1) = g.

    Next, we use the fact that C and the unit circle are orthogonal to get a
    relationship between their radii (pythagorean theorem):

        1^2 + r^2 = g_x^2, where r^2 = (b_x - g_x)^2 + tan(pi / p)^2 b_x^2

    substituting in g = b_x (Z + 1) and solving for b_x,

        b_x = sqrt(1 / (1 + 2Z - (tan(pi / p))^2))

    We can then solve for b_y, g, and d_x trivially.
    """
    tan_p = math.tan(math.pi / p)
    Z = math.tan(math.pi / p + math.pi / q) * tan_p

    b_x = math.sqrt(1 / (1 + 2 * Z - tan_p ** 2))
    b_y = b_x * tan_p
    g_x = b_x * (Z + 1)
    d_x = g_x - math.sqrt(b_y ** 2 + (b_x - g_x) ** 2)

    A = Point(0, 0)
    B = Point(b_x, b_y)
    D = Point(d_x, 0)

    return [A, B, D]


class HyperbolicTessellation(object):

    """A class representing a tessellation in the Poincare disk model.

    The model consists of the interior of a unit disk in the plane. Lines are
    arcs of circles perpendicular to the boundary of the disk.
    """

    def __init__(self,
            configuration,
            center_polygon_radius=0.5,
            num_layers=5):
        self.configuration = configuration
        r = center_polygon_radius

        num_sides = configuration.numPolygonSides
        q = configuration.numPolygonsPerVertex

        # make the fundamental right triangle with angle measures
        # pi / p, pi / q, pi
        # the pi / p angle is at the center
        center = (0, 0)
        bottom_edge_ideal_point = (1, 0)
        top_edge_ideal_point = (cos(pi / num_sides), sin(pi / num_sides))
