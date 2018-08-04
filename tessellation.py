"""The core implementation of a hyperbolic tessellation of the
Poincare disk by uniform, regular polygons.
"""

from collections import deque
from collections import namedtuple
from geometry import Point
from geometry import are_close
from geometry import bounding_box_area
from geometry import orientation
from hyperbolic import PoincareDiskLine
from hyperbolic import PoincareDiskModel
from hyperbolic import compute_fundamental_triangle
import svgwrite


class TessellationConfiguration(
        namedtuple('TessellationConfiguration',
                   ['numPolygonSides', 'numPolygonsPerVertex'])):
    def __init__(self, numPolygonSides, numPolygonsPerVertex):
        if not self.is_hyperbolic():
            raise Exception("Configuration {%s, %s} is not hyperbolic." %
                            (self.numPolygonSides, self.numPolygonsPerVertex))

    def is_hyperbolic(self):
        return (self.numPolygonSides - 2) * (self.numPolygonsPerVertex - 2) > 4


class PolygonSet(list):
    """A helper class wrapping a set of polygons, that implements special
    checks for membership and addition.

    When determining if a polygon has been visited, the order of its vertices
    is irrelevant, so we sort them before adding them to processed.

    Moreover, due to the floating point precision, the entire set of processed
    vertices has to be checked for nearness.
    """

    def add_polygon(self, points):
        self.append(sorted(points))

    def contains_polygon(self, points):
        for p in self:
            if are_close(p, points):
                return True
        return False


class RenderedCoords:
    """A helper class to keep track of a transformation from the unit circle to
    a rendered image.
    """

    def __init__(self, canvas_width):
        self.canvas_width = canvas_width
        self.canvas_center = Point(canvas_width / 2, canvas_width / 2)
        self.scaling_factor = self.canvas_width / 2

    def in_rendered_coords(self, p):
        if isinstance(p, Point):
            scaled_and_reflected = Point(p.x, -p.y) * self.scaling_factor
            return self.canvas_center + scaled_and_reflected
        else:
            return p * self.scaling_factor


class HyperbolicTessellation(object):
    """A class representing a tessellation in the Poincare disk model.

    The model consists of the interior of a unit disk in the plane. Lines are
    arcs of circles perpendicular to the boundary of the disk.
    """

    def __init__(self, configuration, min_area=1e-3):
        self.configuration = configuration
        self.disk_model = PoincareDiskModel(Point(0, 0), radius=1)

        # compute the vertices of the center polygon via reflection
        self.center_polygon = self.compute_center_polygon()
        self.tessellated_polygons = self.tessellate(min_area=min_area)

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
        processed = PolygonSet()

        while queue:
            polygon = queue.pop()
            if bounding_box_area(polygon) < min_area:
                processed.add_polygon(polygon)
                continue

            if processed.contains_polygon(polygon):
                continue

            edges = [(polygon[i], polygon[(i + 1) % len(polygon)])
                     for i in range(len(polygon))]
            for u, v in edges:
                line = self.disk_model.line_through(u, v)
                reflected_polygon = [line.reflect(p) for p in polygon]
                queue.append(reflected_polygon)

            tessellated_polygons.append(polygon)
            processed.add_polygon(polygon)

        return tessellated_polygons

    def render(self, filename, canvas_width):
        """Output an svg file drawing the tessellation."""
        self.transformer = RenderedCoords(canvas_width)
        self.dwg = svgwrite.Drawing(filename=filename, debug=True)

        self.dwg.fill(color='white', opacity=0)
        boundary_circle = self.dwg.circle(
            center=self.transformer.in_rendered_coords(self.disk_model.center),
            r=self.transformer.in_rendered_coords(self.disk_model.radius),
            id='boundary_circle',
            stroke='black',
            stroke_width=1)
        boundary_circle.fill(color='white', opacity=0)
        self.dwg.add(boundary_circle)

        polygon_group = self.dwg.add(self.dwg.g(id='polygons', stroke='blue', stroke_width=1))
        for polygon in self.tessellated_polygons:
            self.render_polygon(polygon, polygon_group)

        self.dwg.save()

    def render_polygon(self, polygon, group):
        arcs_group = group.add(self.dwg.g())

        edges = [(polygon[i], polygon[(i + 1) % len(polygon)])
                 for i in range(len(polygon))]

        for (p, q) in edges:
            line = self.disk_model.line_through(p, q)
            if isinstance(line, PoincareDiskLine):
                self.render_arc(arcs_group, line, p, q)
            else:
                line = self.dwg.line(
                    self.transformer.in_rendered_coords(p),
                    self.transformer.in_rendered_coords(q))
                arcs_group.add(line)

    def render_arc(self, group, line, from_point, to_point):
        use_positive_angle_dir = orientation(
            from_point, to_point, self.disk_model.center) == 'counterclockwise'

        p1 = self.transformer.in_rendered_coords(from_point)
        p2 = self.transformer.in_rendered_coords(to_point)
        r = self.transformer.in_rendered_coords(line.radius)
        circle_center = self.transformer.in_rendered_coords(line.center)
        path = self.dwg.path('m')

        path.push(p1)
        path.push_arc(
            target=p2,
            rotation=0,
            r=r,
            large_arc=False,
            angle_dir='+' if use_positive_angle_dir else '-',
            absolute=True)

        group.add(path)


if __name__ == "__main__":
    config = TessellationConfiguration(6, 4)
    tessellation = HyperbolicTessellation(config)
    tessellation.render(filename="tessellation_6_4.svg", canvas_width=500)
