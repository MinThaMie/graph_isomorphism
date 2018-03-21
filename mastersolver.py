from GI_solver_tools import *
import tools

G = load_file('colorref_smallexample_2_49.grl')
solve(G)
for graph in G:
    write_file(graph)

tools.dot_to_pdf('colorful.dot', 'piemel.pdf', True)
