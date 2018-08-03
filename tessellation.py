"""The core implementation of a hyperbolic tessellation of the
Poincare disk by uniform, regular polygons.
"""

from collections import deque
from collections import namedtuple
from geometry import Point
from geometry import bounding_box_area
from hyperbolic import PoincareDiskModel
from hyperbolic import compute_fundamental_triangle


EPSILON = 1e-6


def are_close(points1, points2):
    for p1, p2 in zip(sorted(points1), sorted(points2)):
        if (p1 - p2).norm() > EPSILON:
            return False
    return True


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
        self.tessellated_polygons = self.tessellate()

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
        for i in range(p - 1):
            p2 = self.disk_model.line_through(center, p1).reflect(p2)
            p1 = self.disk_model.line_through(center, p2).reflect(p1)
            polygon.append(p1)

        return polygon

    def tessellate(self, min_area=1e-3):
        """Return the set of polygons that make up a tessellation of the center
        polygon. Keep reflecting polygons until the Euclidean bounding box of all
        polygons is less than the given threshold.
        """
        queue = deque()
        queue.append(self.center_polygon)
        tessellated_polygons = []

        """When determining if a polygon has been visited, the order of its vertices
        is irrelevant, so we sort them before adding them to processed.

        Moreover, due to the floating point precision, the entire set of processed
        vertices has to be checked for nearness.
        """
        processed = []

        def add_to_processed(points):
            processed.append(sorted(points))

        def is_in_processed(points):
            for p in processed:
                if are_close(set(p), set(points)):
                    return True
            return False

        while queue:
            polygon = queue.pop()
            if bounding_box_area(polygon) < min_area:
                add_to_processed(polygon)
                continue

            if is_in_processed(polygon):
                continue

            edges = [(polygon[i], polygon[(i + 1) % len(polygon)])
                     for i in range(len(polygon))]
            for u, v in edges:
                line = self.disk_model.line_through(u, v)
                reflected_polygon = [line.reflect(p) for p in polygon]
                queue.append(reflected_polygon)

            tessellated_polygons.append(polygon)
            add_to_processed(polygon)

        return tessellated_polygons
