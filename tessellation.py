from math import sin, cos, pi
import geometry


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
