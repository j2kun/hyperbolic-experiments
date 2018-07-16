class TessellationConfiguration(object):
    def __init__(self, numPolygonSides, numPolygonsPerVertex):
        """Create a new configuration

        :numPolygonSides: The number of sides of each polygon.
        :numPolygonsPerVertex: The number of polygons touching each vertex.

        """
        self.numPolygonSides = numPolygonSides
        self.numPolygonsPerVertex = numPolygonsPerVertex

        if not self.is_hyperbolic():
            raise Exception("Configuration {%s, %s} is not hyperbolic." %
                    (self.numPolygonSides, self.numPolygonsPerVertex))

    def is_hyperbolic(self):
        return (self.numPolygonSides - 2) * (self.numPolygonsPerVertex - 2) > 4


class TessellationGraph(object):

    """The graph of polygon edge-vertex adjacencies of a tessellation. A graph
    is organized in levels of concentric layers of vertices representing polygons,
    and there is an edge between two vertices if the corresponding polygons
    share an edge.

    Each layer is a plain list, with vertices oriented so that iterating over
    the list visits the vertices in counterclockwise order, and so that the
    first vertex in each layer is adjacent to the first vertex in the next
    layer and the previous layer.
    """

    def __init__(self, tessellation_configuration, num_layers=2):
        """Construct a graph with the given configuration and num_layers
        layers.
        """
        self.configuration = tessellation_configuration

        # Create the center polygon, which is the first layer.
        center = Vertex(layer=0, index_in_layer=0)
        self.vertices = [center]
        self.layers = [[center]]

        self.create_layers(num_layers)

    def create_layers(self, num_layers):
        for layer_index in range(1, num_layers):
            layer_size = self.compute_layer_size(layer_index)
            new_layer = [
                Vertex(layer=layer_index, index_in_layer=i)
                for i in range(layer_size)
            ]
            self.connect_new_layer(self.layers[-1], new_layer)
            self.layers.append(new_layer)

    def connect_new_layer(self, previous_layer, next_layer):
        p = self.configuration.numPolygonSides
        q = self.configuration.numPolygonsPerVertex

        """Each polygon vertex corresponds to a cycle of length q, so each
        time a vertex connects to the previous layer, the next q-2 vertices are
        skipped before another previous-to-next layer connection. Once a
        preivous layer vertex has achieved its proper degree p, we know to
        attach to the next vertex in the previous layer. Whether a node is
        connected to the previous layer by an edge determines its
        previous_layer_connection_type.
        """
        num_traversed_in_next_layer = 0
        num_traversed_in_previous_layer = 0
        num_traversed_since_previous_layer = 0

        while num_traversed_in_next_layer < len(next_layer):
            next_layer_vertex = next_layer[num_traversed_in_next_layer]
            if len(previous_layer) == 1:
                num_traversed_in_previous_layer = 0
            else:
                """The current vertex we're using to connect the previous layer
                may have become full, or was already full before we visited it
                (such as can occur in a {3, 7} tiling).
                """
                while previous_layer[num_traversed_in_previous_layer].degree == p:
                    num_traversed_in_previous_layer = (num_traversed_in_previous_layer + 1) % len(previous_layer)

            previous_layer_vertex = previous_layer[num_traversed_in_previous_layer]


            if num_traversed_since_previous_layer % (q - 2) == 0:
                previous_layer_vertex.add_edge(next_layer_vertex)
                next_layer_vertex.previous_layer_connection_type = "edge"
            else:
                next_layer_vertex.previous_layer_connection_type = "vertex"

            next_layer_vertex.add_edge(
                next_layer[(num_traversed_in_next_layer + 1) % len(next_layer)])

            num_traversed_since_previous_layer += 1
            num_traversed_in_next_layer += 1

    def compute_layer_size(self, layer_index):
        p = self.configuration.numPolygonSides
        q = self.configuration.numPolygonsPerVertex

        if layer_index == 1:
            """There is one new graph vertex for each polygon edge of the
            center polygon, plus (q-3) new graph vertices for each polygon
            vertex, since there are (q-3) polygons that share a vertex
            (excluding the center polygon, and the two already counted via the
            polygon edges).  This results in p + p(q-3) = p(q-2).
            """
            return p * (q - 2)
        else:
            """Otherwise, we compute based on the previous_layer_connection_types of
            vertices in the previous layer. For both types, only include the
            left-most polygon vertex.

            For "edge" type, there are (p-3) polygon edges and (p-3) polygon
            vertices. Each polygon edge corresponds to a single new graph
            vertex, and each polygon vertex except the left-most corresponds to
            (q-3) new polygon vertices. The left-most, since it is adjacent to
            another polygon in this same layer, corresponds to q-4 new graph
            vertices. With some algebra, the total works out to (p-3)(q-2) - 1.

            For "vertex" type, there is one extra polygon edge and polygon
            vertex, totaling to (p-2)(q-2) - 1.
            """
            return sum(
                (p - 3) * (q - 2) - 1 if vertex.previous_layer_connection_type == "edge"
                else (p - 2) * (q - 2) - 1  # "vertex"
                for vertex in self.layers[layer_index - 1])


class Vertex(object):
    """A vertex is uniquely identified by the pair of its layer index and its position within a layer.

    Each node also has an adjacency type with the previous layer, which is one of:

    - None: for the center vertex
    - "edge": if it shares an edge with a polygon in the previous layer, and
      hence has such an edge in the graph.
    - "vertex": if it only meets the previous layer at a vertex, and hence
      there is no edge between this vertex and the previous layer.
    """
    def __init__(self, layer, index_in_layer):
        self.layer = layer
        self.index_in_layer = index_in_layer
        self.previous_layer_connection_type = None
        self.edges = []

    @property
    def degree(self):
        return len(self.edges)

    def is_adjacent_to(self, vertex):
        return sum(1 for e in self.edges if e.contains(vertex)) > 0

    def add_edge(self, vertex):
        e = Edge(self, vertex)
        self.edges.append(e)
        vertex.edges.append(e)

    def __str__(self):
        return "Vertex(layer={}, index={})".format(self.layer, self.index_in_layer)


class Edge(object):
    def __init__(self, v, w):
        self.incident_vertices = [v, w]

    def other(self, vertex):
        """Return the vertex incident to this edge which is not the given vertex."""
        if self.incident_vertices[0] == vertex:
            return self.incident_vertices[1]

        if self.incident_vertices[1] == vertex:
            raise Exception("Supplied a vertex not a member of this edge. "
                    "edge={}, vertex={}".format(self, vertex))

        return self.incident_vertices[0]

    def contains(self, vertex):
        return vertex in self.incident_vertices

    def __str__(self):
        return "Edge({}, {})".format(*self.incident_vertices)
