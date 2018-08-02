"""The core implementation of a hyperbolic tessellation of the
Poincare disk by uniform, regular polygons.
"""

from hyperbolic import PoincareDiskModel
from hyperbolic import compute_fundamental_triangle


class HyperbolicTessellation(object):

    """A class representing a tessellation in the Poincare disk model.

    The model consists of the interior of a unit disk in the plane. Lines are
    arcs of circles perpendicular to the boundary of the disk.
    """

    def __init__(self, configuration):
        self.configuration = configuration
        self.disk_model = PoincareDiskModel(Point(0, 0), radius=1)

        center, top_vertex, x_axis_vertex = compute_fundamental_triangle(configuration)

        # compute the vertices of the center polygon via reflection
        self.center_polygon = self.compute_center_polygon(center, top_vertex, x_axis_vertex)

    def compute_center_polygon(self, center, top_vertex, x_axis_vertex):
        p = self.configuration.numPolygonSides

        """The center polygon's first vertex is the top vertex (the one that
        makes an angle of pi / q), because the x_axis_vertex is the center of
        an edge.
        """
        polygon = [top_vertex]

        p1, p2 = top_vertex, x_axis_vertex
        for i in range(p):
            p2 = self.disk_model.line_through(center, p1).reflect(p2)
            polygon.append(p2)
            p1 = self.disk_model.line_through(center, p2).reflect(p1)

        assert len(polygon) == p
        return p
