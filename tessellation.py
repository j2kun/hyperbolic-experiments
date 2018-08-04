"""The core implementation of a hyperbolic tessellation of the
Poincare disk by uniform, regular polygons.
"""

from collections import deque
from collections import namedtuple
from geometry import Point
from geometry import bounding_box_area
from hyperbolic import PoincareDiskModel
from hyperbolic import compute_fundamental_triangle
import svgwrite


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
                if are_close(p, points):
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

    def render(self, filename, canvas_width):
        """Output an svg file drawing the tessellation."""
        canvas_center = Point(canvas_width / 2, canvas_width / 2)

        def in_rendered_coords(p):
            if isinstance(p, Point):
                scaled_and_reflected = Point(p.x, -p.y) * canvas_width
                return canvas_center + scaled_and_reflected
            else:
                return p * canvas_width

        dwg = svgwrite.Drawing(filename=filename, debug=True)
        dwg.fill(color='white', opacity=0)
        boundary_circle = dwg.circle(
            center=in_rendered_coords(self.disk_model.center),
            r=in_rendered_coords(self.disk_model.radius),
            id='boundary_circle',
            stroke='black',
            stroke_width=1)
        boundary_circle.fill(color='white', opacity=0)
        dwg.add(boundary_circle)

        polygon_group = dwg.add(dwg.g(id='polygons', stroke='blue', stroke_width=1))
        for polygon in self.tessellated_polygons:
            self.render_polygon(polygon, dwg, polygon_group)

        dwg.save()

    def render_polygon(self, polygon, dwg, group):
        arcs_group = group.add(dwg.g())

        edges = [(polygon[i], polygon[(i + 1) % len(polygon)])
                 for i in range(len(polygon))]

        for (p, q) in edges:
            line = self.disk_model.line_through(p, q)
            if isinstance(line, PoincareDiskLine):
                render_arc(dwg, arcs_group, line, p, q)
            else:
                line = dwg.line(render(p), render(q))
                arcs_group.add(line)

    def render_arc(self, dwg, group, line, from_point, to_point):
        use_positive_angle_dir = orientation(
            from_point, to_point, self.disk_model.center) == 'clockwise'

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
