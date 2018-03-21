from GI_solver_tools import *
import tools

filename = 'colorref_smallexample_2_49'

G = load_file(filename + '.grl')
solve(G, [])
for graph in G:
    write_file(graph)

tools.dot_to_pdf('colorful.dot', filename + '_solved.pdf', False)
