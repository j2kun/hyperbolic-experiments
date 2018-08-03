from collections import deque


class TessellationGraph(object):

    """The graph of polygon edge-vertex adjacencies of a tessellation. A graph
    is organized in levels of concentric layers of vertices representing polygons,
    and there is an edge between two vertices if the corresponding polygons
    share an edge.

    Each layer is a plain list, with vertices oriented so that iterating over
    the list visits the vertices in counterclockwise order, and so that the
    first vertex in each layer is adjacent to the first (allowable) vertex in
    the next layer.
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

    def vertex_at(self, layer, index_in_layer):
        return self.layers[layer][index_in_layer]

    def create_layers(self, num_layers):
        for layer_index in range(1, num_layers):
            layer_size = self.compute_layer_size(layer_index)
            new_layer = [
                Vertex(layer=layer_index, index_in_layer=i)
                for i in range(layer_size)
            ]
            self.connect_layer(self.layers[-1], new_layer)
            self.layers.append(new_layer)
            self.vertices.extend(new_layer)

        self.connect_cyclic_only(self.layers[-1])

    def connect_layer(self, this_layer, next_layer):
        """Connect the vertices in next_layer to the vertices in
        this_layer, and connect the edges among vertices in this_layer.

        To ensure that the edge list produced is ordered counterclockwise
        around each vertex, (though this class does not enforce any geometry,
        the ordering choices we make give guarantees for the Poincare disk
        model), for each vertex in this_layer we add edges in the following
        order:

        1. If this_layer is not the first layer, then there will be an existing edge
           from a previous invocation of this method.
        2. The previous vertex in the cyclic ordering of this_layer.
        3. The relevant vertices in next_layer, in the cyclic order of next_layer.
        4. The next vertex in the cyclic ordering of this_layer.
        """

        p = self.configuration.numPolygonSides
        q = self.configuration.numPolygonsPerVertex

        """Initialize two queues for each layer, and we will advance through the
        queues as the degree of each vertex is filled up.
        """

        this_layer_queue = deque(this_layer)
        next_layer_queue = deque(next_layer)

        while this_layer_queue:
            this_layer_vertex = this_layer_queue.popleft()

            """(2), (4) join this_layer_vertex to the previous vertex in the
            ordering of this_layer.

            The special edge addition strategy of add_cyclic_edge causes the
            same result as if (4) was done after (3).
            """
            # The center vertex has no within-layer edges
            if this_layer_vertex.layer > 0:
                self.add_cyclic_edge(this_layer_vertex, this_layer)

            """(3) join this_layer_vertex to the relevant vertices in
            next_layer.

            Since this_layer_vertex doesn't yet have an edge
            to the next vertex in this_layer, its "maximal" degree is p-1.
            However, at the very end of the process (when this_layer_queue
            is empty), the last vertex in this_layer to process will have
            the extra forward edge, so we adjust for that.
            """
            if this_layer_vertex.layer == 0 or not this_layer_queue:
                maximal_degree = p
            else:
                maximal_degree = p - 1

            while this_layer_vertex.degree < maximal_degree:
                # add the edge connection to the next layer
                next_layer_vertex = next_layer_queue.popleft()
                this_layer_vertex.add_edge(next_layer_vertex)
                next_layer_vertex.previous_layer_connection_type = "edge"

                """There are two cases. In the normal case, we add one edge to
                a next_layer_vertex, then skip q - 3 subsequent vertices in
                next_layer that share only a vertex with this_layer_vertex.

                This rule is violated in multiple instances, such as in layer 0
                or being the last vertex processed in a layer. All of the
                exceptional cases are covered by checking to see if the current
                degree of a vertex is maximal, according to the maximal_degree
                rule computed above.

                Finally because it can happen in some configurations that the
                next vertex in this_layer is already full (e.g., in a {3, 7}
                tiling some vertices in layer 1 will only have edges within the
                layer and to layer 0) we check to see if the next vertex in
                this_layer will be skipped.
                """
                if this_layer_vertex.degree == maximal_degree:
                    num_vertices_to_skip = q - 4
                    if len(this_layer_queue) > 1 and this_layer_queue[0].degree == p - 2:
                        num_vertices_to_skip -= 1
                else:
                    num_vertices_to_skip = q - 3

                for i in range(num_vertices_to_skip):
                    next_layer_vertex = next_layer_queue.popleft()
                    next_layer_vertex.previous_layer_connection_type = "vertex"
                    if not next_layer_queue:
                        break

    def connect_cyclic_only(self, layer):
        for vertex in layer:
            self.add_cyclic_edge(vertex, layer)

    def add_cyclic_edge(self, this_layer_vertex, this_layer):
        """Add an edge between this_layer_vertex and the previous vertex in the
        cyclic ordering of this_layer.

        To maintain the ordering property, we append the edge to one edge list,
        and prepend to the other's edge list.
        """
        previous_vertex = this_layer[(this_layer_vertex.index_in_layer - 1) % len(this_layer)]
        if not this_layer_vertex.is_adjacent_to(previous_vertex):
            e = Edge(this_layer_vertex, previous_vertex)
            this_layer_vertex.edges.append(e)
            previous_vertex.edges.appendleft(e)

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
        self.edges = deque()

    @property
    def degree(self):
        return len(self.edges)

    def add_edge(self, vertex):
        print("Adding edge between %s and %s" % (self, vertex))
        e = Edge(self, vertex)
        self.edges.append(e)
        vertex.edges.append(e)

    def __str__(self):
        return "v_{},{}".format(self.layer, self.index_in_layer)
        # return "Vertex(layer={}, index={})".format(self.layer, self.index_in_layer)

    def __repr__(self):
        return str(self)

    def is_adjacent_to(self, vertex):
        return sum(1 for e in self.edges if e.contains(vertex)) > 0


class Edge(object):
    def __init__(self, v, w):
        self.incident_vertices = [v, w]

    def __str__(self):
        return "Edge({}, {})".format(*self.incident_vertices)

    def contains(self, vertex):
        return vertex in self.incident_vertices


'''
    def other(self, vertex):
        """Return the vertex incident to this edge which is not the given vertex."""
        if self.incident_vertices[0] == vertex:
            return self.incident_vertices[1]

        if self.incident_vertices[1] == vertex:
            raise Exception("Supplied a vertex not a member of this edge. "
                    "edge={}, vertex={}".format(self, vertex))

        return self.incident_vertices[0]
'''
