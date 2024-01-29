
import os 
import sys 
sys.path.insert(0, os.path.abspath('../src'))

def get_version(rel_path):
    """Get the version string from a file.
    Assuming the version line is in the form: __version__ = '0.1.0'
    strips out the version and remove leading and trailing whitespace and quotes
    Args:
        rel_path (str): The relative path to the file.
Raises:
    RuntimeError: If the version string is not found.

	Returns:
        str: The version string.
    """

    with open(rel_path, 'r', encoding='utf-8') as fp:
        for line in fp:
            if line.startswith('__version__'):
                delim = '"' if '"' in line else "'"
                return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")

PATH_TO_INIT_PY = '../../src/npp_2d_truss_analysis/__init__.py'

__version__ = get_version(PATH_TO_INIT_PY)

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'NPP 2d Truss Analysis'
copyright = '2024, Nikolaos Papadakis'
author = 'Nikolaos Papadakis'
release = __version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']



rst_epilog = """
.. |ProjectVersion| replace:: v{versionnum}
""".format(versionnum = release
)