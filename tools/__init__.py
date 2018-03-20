import os


def dot_to_pdf(dot_file_path: str, pdf_file_path: str, open_outfile: bool = False):
    """Read a Graphviz DOT file and write to PDF."""

    os.system(f'dot {dot_file_path} -Tpdf > {pdf_file_path}')

    if open_outfile:
        os.system(f'open {pdf_file_path}')
