# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import sys
sys.path.insert(0, '../')
sys.path.insert(0, '../src/')
sys.path.insert(0, '../src/pg_engine')
sys.path.insert(0, '../src/pg_engine/base_scripts')
sys.path.insert(0, '../src/pg_engine/components')
sys.path.insert(0, '../src/pg_engine/core')
sys.path.insert(0, '../src/pg_engine/core/bases')
sys.path.insert(0, '../src/pg_engine/core/loaders')
sys.path.insert(0, '../src/pg_engine/core/processors')
sys.path.insert(0, '../src/pg_engine/logging')
sys.path.insert(0, '../src/pg_engine/systems')

project = 'PG_Engine'
copyright = '2025, Kenzo Staelens'
author = 'Kenzo Staelens'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.autosummary',
    'sphinx_toolbox.collapse',
    'sphinx_toolbox.more_autodoc.generic_bases',
    'sphinx_toolbox.more_autodoc.typevars',
]

autosummary_generate = True

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

intersphinx_mapping = {
    'pygame': ('https://www.pygame.org/docs/', None),
    'pygame_gui': ('https://pygame-gui.readthedocs.io/en/latest/', None)
}
