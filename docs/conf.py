# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import datetime

project = 'PeakRDL Extension for Sphinx-Doc'
copyright = '%d, Alex Mykyta' % datetime.datetime.now().year
author = 'Alex Mykyta'
html_title = project

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.todo",
    "sphinx_peakrdl",
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

todo_include_todos = True
todo_emit_warnings = True

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_book_theme"
html_theme_options = {
    "repository_url": "https://github.com/SystemRDL/sphinx-peakrdl",
    "path_to_docs": "docs",
    "use_download_button": False,
    "use_source_button": True,
    "use_repository_button": True,
    "use_issues_button": True,
    "announcement": (
        "⚠️ This extension is still in early development. "
        "If you have ideas on what could be improved, let me know! ⚠️"
    ),
}
html_static_path = []

# -- PeakRDL config ------------------------------------------------------------
peakrdl_input_files = [
    "rdl_src/uart.rdl",
    "rdl_src/turboencabulator.rdl",
    "rdl_src/thingamabob.rdl",
    "rdl_src/my_soc_top.rdl",
]
