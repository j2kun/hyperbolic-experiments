import itertools

from tessellation import *


def test_valid_configuration():
    TessellationConfiguration(6, 4)
    TessellationConfiguration(4, 5)
    TessellationConfiguration(7, 3)
    TessellationConfiguration(3, 7)


def test_invalid_configuration():
    try:
        TessellationConfiguration(4, 4)
        assert False
    except:
        pass


def test_three_layer_tessellation_graph_6_4():
    graph = TessellationGraph(TessellationConfiguration(6, 4), num_layers=3)
    assert len(graph.layers) == 3
    assert len(graph.layers[0]) == 1
    assert len(graph.layers[1]) == 12
    assert len(graph.layers[2]) == 72

    all_vertices = [(n.layer, n.index_in_layer) for n in graph.vertices]

    within_second_layer = [((1, i), (1, (i + 1) % 12)) for i in range(12)]
    within_third_layer = [((2, i), (2, (i + 1) % 72)) for i in range(72)]
    first_layer_to_second_layer = [
        ((0,0), (1,0)),
        ((0,0), (1,2)),
        ((0,0), (1,4)),
        ((0,0), (1,6)),
        ((0,0), (1,8)),
        ((0,0), (1,10)),
    ]

    second_layer_to_third_layer = [
        ((1,0), (2,0)),
        ((1,0), (2,1)),
        ((1,0), (2,2)),
        ((1,0), (2,3)),
        ((1,0), (2,4)),
        ((1,1), (2,5)),
        ((1,1), (2,6)),
        ((1,1), (2,7)),
        ((1,1), (2,8)),
        ((1,1), (2,9)),
        ((1,1), (2,10)),
        ((1,1), (2,11)),
        ((1,2), (2,12)),
        ((1,2), (2,13)),
        ((1,2), (2,14)),
        ((1,2), (2,15)),
        ((1,2), (2,16)),
        ((1,3), (2,17)),
        ((1,3), (2,18)),
        ((1,3), (2,19)),
        ((1,3), (2,20)),
        ((1,3), (2,21)),
        ((1,3), (2,22)),
        ((1,3), (2,23)),
        ((1,4), (2,24)),
        ((1,4), (2,25)),
        ((1,4), (2,26)),
        ((1,4), (2,27)),
        ((1,4), (2,28)),
        ((1,5), (2,29)),
        ((1,5), (2,30)),
        ((1,5), (2,31)),
        ((1,5), (2,32)),
        ((1,5), (2,33)),
        ((1,5), (2,34)),
        ((1,5), (2,35)),
        ((1,5), (2,29)),
        ((1,5), (2,30)),
        ((1,5), (2,31)),
        ((1,5), (2,32)),
        ((1,5), (2,33)),
        ((1,5), (2,34)),
        ((1,5), (2,35)),
        ((1,6), (2,36)),
        ((1,6), (2,37)),
        ((1,6), (2,38)),
        ((1,6), (2,39)),
        ((1,6), (2,40)),
        ((1,7), (2,41)),
        ((1,7), (2,42)),
        ((1,7), (2,43)),
        ((1,7), (2,44)),
        ((1,7), (2,45)),
        ((1,7), (2,46)),
        ((1,7), (2,47)),
        ((1,8), (2,48)),
        ((1,8), (2,49)),
        ((1,8), (2,50)),
        ((1,8), (2,51)),
        ((1,8), (2,52)),
        ((1,9), (2,53)),
        ((1,9), (2,54)),
        ((1,9), (2,55)),
        ((1,9), (2,56)),
        ((1,9), (2,57)),
        ((1,9), (2,58)),
        ((1,9), (2,59)),
        ((1,10), (2,60)),
        ((1,10), (2,61)),
        ((1,10), (2,62)),
        ((1,10), (2,63)),
        ((1,10), (2,64)),
        ((1,11), (2,65)),
        ((1,11), (2,66)),
        ((1,11), (2,67)),
        ((1,11), (2,68)),
        ((1,11), (2,69)),
        ((1,11), (2,70)),
        ((1,11), (2,71)),
    ]

    edges = set(within_second_layer + within_third_layer
        + first_layer_to_second_layer + second_layer_to_third_layer)

    for v1, v2 in itertools.combinations(all_vertices, 2):
        if (v1, v2) in edges or (v2, v1) in edges:
            assert v1.is_adjacent_to(v2)
        else:
            assert not v1.is_adjacent_to(v2)


def test_three_layer_tessellation_graph_3_7():
    graph = TessellationGraph(TessellationConfiguration(3, 7), num_layers=3)
    assert len(graph.layers) == 3
    assert len(graph.layers[0]) == 1
    assert len(graph.layers[1]) == 15
    assert len(graph.layers[2]) == 45

    all_vertices = [(n.layer, n.index_in_layer) for n in graph.vertices]

    within_second_layer = [((1, i), (1, (i + 1) % 15)) for i in range(15)]
    within_third_layer = [((2, i), (2, (i + 1) % 45)) for i in range(45)]
    first_layer_to_second_layer = [
        ((0,0), (1,0)),
        ((0,0), (1,5)),
        ((0,0), (1,10)),
    ]

    second_layer_to_third_layer = [
        ((1,1), (2,0)),
        ((1,2), (2,4)),
        ((1,3), (2,8)),
        ((1,4), (2,12)),
        ((1,6), (2,15)),
        ((1,7), (2,19)),
        ((1,8), (2,23)),
        ((1,9), (2,27)),
        ((1,11), (2,30)),
        ((1,12), (2,34)),
        ((1,13), (2,38)),
        ((1,14), (2,42)),
    ]

    edges = set(within_second_layer + within_third_layer
        + first_layer_to_second_layer + second_layer_to_third_layer)

    for v1, v2 in itertools.combinations(all_vertices, 2):
        if (v1, v2) in edges or (v2, v1) in edges:
            assert v1.is_adjacent_to(v2)
        else:
            assert not v1.is_adjacent_to(v2)