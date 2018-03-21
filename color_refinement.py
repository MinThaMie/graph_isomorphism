import os

import time

from graph_io import load_graph, write_dot

GRAPHS_FOLDER = 'graphs'
EXPORT_FOLDER = 'export'

FILE_NAME = 'colorref_smallexample_4_16'


def main():
    color = 0
    g = 0
    graphs = open_file()[g]
    colored_sets = initial_coloring(graphs[0], color)  # TODO loop through all graphs
    changed = True
    start_time = time.time()
    while changed:
        some_change = False
        for colorset in list(colored_sets):
            new_colorsets = refine(colored_sets[colorset], color)
            if len(new_colorsets) > 0:
                colored_sets.update(new_colorsets)
                some_change = True
        changed = some_change
    total_time = time.time() - start_time

    export_graph(graphs[g], g)
    print("Time: " + str(total_time))
    print("Isomorphs: " + str(count(colored_sets)))
    # export_graphs(graphs)


def count(colored_sets):
    n = 1
    for colorset in colored_sets:
        n * len(colored_sets[colorset])
    return n


def initial_coloring(graph, color):
    initial_sets = {}
    for v in graph.vertices:
        if v.degree in initial_sets:
            initial_sets[v.degree].add(v)
        else:
            initial_sets[v.degree] = {v}
        v.set_color(v.degree)
        if v.degree >= color:
            color = v.degree + 1
    return initial_sets


def refine(colorset, color):
    v0 = colorset.pop()
    temp_set = set()
    new_colorsets = {}
    for i in range(1, len(colorset)):
        vertex = colorset.pop()
        if not is_same(v0, vertex):
            added_to_existing = False
            for new_set_i in new_colorsets:
                new_set = new_colorsets[new_set_i]
                for v in new_set:
                    if is_same(v, vertex):
                        new_set.add(vertex)
                        vertex.set_color(v.color)
                        added_to_existing = True
                        break
                if added_to_existing:
                    break
            if not added_to_existing:
                new_colorset = set()
                new_colorset.add(vertex)
                new_colorsets[color] = new_colorset
                vertex.set_color(color)
                color += 1
        else:
            temp_set.add(vertex)
    for temp in temp_set:
        colorset.add(temp)
    colorset.add(v0)
    return new_colorsets


def get_neighbour_colors(vertex):
    v_colors = []
    for n in vertex.neighbours:
        v_colors.append(n.color)
    return v_colors


def is_same(v0, vn):
    return get_neighbour_colors(v0) == get_neighbour_colors(vn)


def open_file():
    with open(GRAPHS_FOLDER + '/' + FILE_NAME + '.grl') as f:
        return load_graph(f, read_list=True)


def export_graphs(graphs):
    i = 0
    for graph in graphs:
        export_graph(graph, i)
        i += 1


def export_graph(graph, i):
    file = EXPORT_FOLDER + '/' + FILE_NAME + '_' + str(i)
    with open(file + '.dot', 'w') as f:
        write_dot(graph, f)
    os.system('dot -Tpdf ' + file + '.dot -o ' + file + '.pdf')


if __name__ == "__main__":
    main()
