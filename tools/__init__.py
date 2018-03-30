import os
from typing import Dict, Set

_last_integer = 0
_generated_integers = set()


def dot_to_pdf(dot_file_path: str, pdf_file_path: str, open_outfile: bool = False):
    """Read a Graphviz DOT file and write to PDF. `dot` must be on your system path.
    :param str dot_file_path: path to DOT file to read.
    :param str pdf_file_path: path to PDF file to write.
    :param bool open_outfile: open created PDF file if `True`; don't open it otherwise.
    """

    os.system(f'dot {dot_file_path} -Tpdf > {pdf_file_path}')

    if open_outfile:
        os.system(f'open {pdf_file_path}')


def unique_integer() -> int:
    """Generate a unique non-negative integer."""

    # Note: int is unbounded (no max, except for system limit) in Python 3
    # Source: https://stackoverflow.com/a/7604981/3169029

    global _last_integer, _generated_integers

    if _last_integer in _generated_integers:
        _last_integer += 1
        return unique_integer()

    _generated_integers.add(_last_integer)
    return _last_integer


def store_morphism(i: int, j: int, dict_of_pairs: Dict[int, Set[int]]):
    """
    Store a known morphism between two indices in the specified mapping.

    :param int i: Index of one known morphism pair member.
    :param int j: Index of another known morphism pair member.
    :param dict dict_of_pairs: Dictionary in which to store the set of known morphisms.
    """

    morphisms = set()

    for index in (i, j):
        morphisms |= dict_of_pairs[index]

    morphisms |= {i, j}

    for index in morphisms:
        dict_of_pairs[index] = morphisms - {index}
