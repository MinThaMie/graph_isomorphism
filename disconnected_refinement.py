from color_refinement import is_isomorphisms
from graph import Graph
from preprocessing import checks


def graph_component_isomorphic(g: [Graph], h: [Graph]) -> bool:
    """
    compares subgraphs in 2 graphs

        :param g: a list of subgraphs
        :param h: a list of subgraphs
        :return: boolean: True if all preprocessing checks pass
        """
    if len(g) != len(h):
        return False

    for g_subgraph in g:
        sub_graphs_isomorphism = False
        for h_subgraph in h:
            if checks(g_subgraph, h_subgraph):
                if is_isomorphisms(g_subgraph, h_subgraph):
                    sub_graphs_isomorphism = True
        if not sub_graphs_isomorphism:
            return False
    return True
