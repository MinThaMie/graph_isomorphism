import os


def dot_to_pdf(dot_file_path: str, pdf_file_path: str, open_outfile: bool = False):
    """Read a Graphviz DOT file and write to PDF. `dot` must be on your system path.
    :param str dot_file_path: path to DOT file to read.
    :param str pdf_file_path: path to PDF file to write.
    :param bool open_outfile: open created PDF file if `True`; don't open it otherwise.
    """

    os.system(f'dot {dot_file_path} -Tpdf > {pdf_file_path}')

    if open_outfile:
        os.system(f'open {pdf_file_path}')
