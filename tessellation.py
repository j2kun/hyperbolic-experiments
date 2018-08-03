"""The core implementation of a hyperbolic tessellation of the
Poincare disk by uniform, regular polygons.
"""

from collections import namedtuple
from geometry import Point
from hyperbolic import PoincareDiskModel
from hyperbolic import compute_fundamental_triangle


class TessellationConfiguration(
        namedtuple('TessellationConfiguration',
                   ['numPolygonSides', 'numPolygonsPerVertex'])):
    def __init__(self, numPolygonSides, numPolygonsPerVertex):
        if not self.is_hyperbolic():
            raise Exception("Configuration {%s, %s} is not hyperbolic." %
                            (self.numPolygonSides, self.numPolygonsPerVertex))

    def is_hyperbolic(self):
        return (self.numPolygonSides - 2) * (self.numPolygonsPerVertex - 2) > 4


class HyperbolicTessellation(object):

    """A class representing a tessellation in the Poincare disk model.

    The model consists of the interior of a unit disk in the plane. Lines are
    arcs of circles perpendicular to the boundary of the disk.
    """

    def __init__(self, configuration):
        self.configuration = configuration
        self.disk_model = PoincareDiskModel(Point(0, 0), radius=1)

        # compute the vertices of the center polygon via reflection
        self.center_polygon = self.compute_center_polygon()

    def compute_center_polygon(self):
        center, top_vertex, x_axis_vertex = compute_fundamental_triangle(
            self.configuration)
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

        return polygon
