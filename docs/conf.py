# -*- coding: utf-8 -*-
import sys
import os

# Add the Sappho repository directory to the module
# search path
sys.path.insert(0, os.path.abspath('..'))

# Project information
project = u'Sappho'
copyright = u'2016, Hypatia Software Organization'
author = u'Hypatia Software Organization'

# Read the version information from the Sappho code
sappho_init_path = os.path.join(os.path.abspath('..'),
                                'sappho',
                                '__init__.py') 

locals = {}
exec(open(sappho_init_path).read(),
     {"__name__": "__main__"}, 
     locals)

version = ".".join(locals["__version__"].split(".")[0:2])
release = locals["__version__"]

# Sphinx extensions
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    'sphinx.ext.intersphinx',
    'sphinxcontrib.napoleon',
]

# Other Sphinx options
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# Output style options
pygments_style = 'sphinx'
html_theme = 'alabaster'
html_static_path = ['_static']

# Intersphinx mapping
intersphinx_mapping = {
    'python': ('https://docs.python.org/3.4', None),
    'pygame': ('http://www.pygame.org/docs', None),
}
