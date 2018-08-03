import itertools

from tessellation import TessellationConfiguration
from tessellation_graph import *


def assert_edges_are_exactly(graph, edges):
    all_vertices = [(n.layer, n.index_in_layer) for n in graph.vertices]
    for v1, v2 in itertools.combinations(all_vertices, 2):
        vertex1 = graph.vertex_at(v1[0], v1[1])
        vertex2 = graph.vertex_at(v2[0], v2[1])
        if (v1, v2) in edges or (v2, v1) in edges:
            assert vertex1.is_adjacent_to(vertex2)
        else:
            assert not vertex1.is_adjacent_to(vertex2)


def test_three_layer_tessellation_graph_6_4():
    graph = TessellationGraph(TessellationConfiguration(6, 4), num_layers=3)
    assert len(graph.layers) == 3
    assert len(graph.layers[0]) == 1
    assert len(graph.layers[1]) == 12
    assert len(graph.layers[2]) == 72
    assert len(graph.vertices) == 1 + 12 + 72

    within_second_layer = [((1, i), (1, (i + 1) % 12)) for i in range(12)]
    within_third_layer = [((2, i), (2, (i + 1) % 72)) for i in range(72)]
    first_layer_to_second_layer = [
        ((0, 0), (1, 0)),
        ((0, 0), (1, 2)),
        ((0, 0), (1, 4)),
        ((0, 0), (1, 6)),
        ((0, 0), (1, 8)),
        ((0, 0), (1, 10)),
    ]

    second_layer_to_third_layer = [
        ((1, 0), (2, 0)),
        ((1, 0), (2, 2)),
        ((1, 0), (2, 4)),
        ((1, 1), (2, 5)),
        ((1, 1), (2, 7)),
        ((1, 1), (2, 9)),
        ((1, 1), (2, 11)),
        ((1, 2), (2, 12)),
        ((1, 2), (2, 14)),
        ((1, 2), (2, 16)),
        ((1, 3), (2, 17)),
        ((1, 3), (2, 19)),
        ((1, 3), (2, 21)),
        ((1, 3), (2, 23)),
        ((1, 4), (2, 24)),
        ((1, 4), (2, 26)),
        ((1, 4), (2, 28)),
        ((1, 5), (2, 29)),
        ((1, 5), (2, 31)),
        ((1, 5), (2, 33)),
        ((1, 5), (2, 35)),
        ((1, 6), (2, 36)),
        ((1, 6), (2, 38)),
        ((1, 6), (2, 40)),
        ((1, 7), (2, 41)),
        ((1, 7), (2, 43)),
        ((1, 7), (2, 45)),
        ((1, 7), (2, 47)),
        ((1, 8), (2, 48)),
        ((1, 8), (2, 50)),
        ((1, 8), (2, 52)),
        ((1, 9), (2, 53)),
        ((1, 9), (2, 55)),
        ((1, 9), (2, 57)),
        ((1, 9), (2, 59)),
        ((1, 10), (2, 60)),
        ((1, 10), (2, 62)),
        ((1, 10), (2, 64)),
        ((1, 11), (2, 65)),
        ((1, 11), (2, 67)),
        ((1, 11), (2, 69)),
        ((1, 11), (2, 71)),
    ]

    edges = set(within_second_layer + within_third_layer
                + first_layer_to_second_layer + second_layer_to_third_layer)

    assert_edges_are_exactly(graph, edges)


def test_four_layer_tessellation_graph_3_7():
    graph = TessellationGraph(TessellationConfiguration(3, 7), num_layers=4)
    assert len(graph.layers) == 4
    assert len(graph.layers[0]) == 1
    assert len(graph.layers[1]) == 15
    assert len(graph.layers[2]) == 45
    assert len(graph.layers[3]) == 120
    assert len(graph.vertices) == 1 + 15 + 45 + 120

    all_vertices = [(n.layer, n.index_in_layer) for n in graph.vertices]

    within_second_layer = [((1, i), (1, (i + 1) % 15)) for i in range(15)]
    within_third_layer = [((2, i), (2, (i + 1) % 45)) for i in range(45)]
    within_fourth_layer = [((3, i), (3, (i + 1) % 120)) for i in range(120)]
    first_layer_to_second_layer = [
        ((0, 0), (1, 0)),
        ((0, 0), (1, 5)),
        ((0, 0), (1, 10)),
    ]

    second_layer_to_third_layer = [
        ((1, 1), (2, 0)),
        ((1, 2), (2, 4)),
        ((1, 3), (2, 8)),
        ((1, 4), (2, 12)),
        ((1, 6), (2, 15)),
        ((1, 7), (2, 19)),
        ((1, 8), (2, 23)),
        ((1, 9), (2, 27)),
        ((1, 11), (2, 30)),
        ((1, 12), (2, 34)),
        ((1, 13), (2, 38)),
        ((1, 14), (2, 42)),
    ]

    third_layer_to_fourth_layer = [
        ((2, 1), (3, 0)),
        ((2, 2), (3, 4)),
        ((2, 3), (3, 8)),
        ((2, 5), (3, 11)),
        ((2, 6), (3, 15)),
        ((2, 7), (3, 19)),
        ((2, 9), (3, 22)),
        ((2, 10), (3, 26)),
        ((2, 11), (3, 30)),
        ((2, 13), (3, 33)),
        ((2, 14), (3, 37)),
        ((2, 16), (3, 40)),
        ((2, 17), (3, 44)),
        ((2, 18), (3, 48)),
        ((2, 20), (3, 51)),
        ((2, 21), (3, 55)),
        ((2, 22), (3, 59)),
        ((2, 24), (3, 62)),
        ((2, 25), (3, 66)),
        ((2, 26), (3, 70)),
        ((2, 28), (3, 73)),
        ((2, 29), (3, 77)),
        ((2, 31), (3, 80)),
        ((2, 32), (3, 84)),
        ((2, 33), (3, 88)),
        ((2, 35), (3, 91)),
        ((2, 36), (3, 95)),
        ((2, 37), (3, 99)),
        ((2, 39), (3, 102)),
        ((2, 40), (3, 106)),
        ((2, 41), (3, 110)),
        ((2, 43), (3, 113)),
        ((2, 44), (3, 117)),
    ]

    edges = set(
        within_second_layer
        + within_third_layer
        + within_fourth_layer
        + first_layer_to_second_layer
        + second_layer_to_third_layer
        + third_layer_to_fourth_layer
    )

    for vertex in graph.vertices:
        print(vertex)
        for edge in vertex.edges:
            print(edge)
        print()

    assert_edges_are_exactly(graph, edges)
