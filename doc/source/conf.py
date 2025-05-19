# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "UFS Land DA User's Guide"
copyright = '2024, '
author = ' '

# The short X.Y version
version = 'develop'
# The full version, including alpha/beta/rc tags
release = 'develop'

numfig = True

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx_rtd_theme',
    'sphinx.ext.intersphinx',
    'sphinx.ext.extlinks',
    'sphinxcontrib.bibtex',
]

# File with bibliographic info
bibtex_bibfiles = ['references.bib']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The master toctree document.
master_doc = 'index'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# Documentation-wide substitutions

rst_prolog = """
.. |latestr| replace:: v2.0.0
.. |tag| replace:: ``ufs-land-da-v2.0.0``
.. |branch| replace:: ``release/public-v2.0.0``
.. |skylabv| replace:: Skylab v8.0
.. |spack-stack-ver| replace:: v1.6.0
.. |data| replace:: v2.1
"""

# -- Linkcheck options -------------------------------------------------

# Avoid a 403 Forbidden error when accessing certain links (e.g., noaa.gov)
# Can be found using navigator.userAgent inside a browser console.
user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"

# Ignore working links that cause a linkcheck 403 error.
linkcheck_ignore = [r'https://www\.intel\.com/content/www/us/en/developer/tools/oneapi/hpc\-toolkit\-download\.html',
                    r'https://doi.org/10.1029/.*',
                    r'https://doi.org/10.1002/.*',
                    r'https://doi.org/10.5281/zenodo.13909475', # DOI not published until release
                    r'https://sourceforge.net/projects/xming/',
                    ]

# Ignore anchor tags for Land DA data bucket. Shows Not Found even when they exist.
linkcheck_anchors_ignore = []

linkcheck_allowed_redirects = {r"https://github.com/ufs-community/land-DA_workflow/wiki/.*": 
                                 r"https://raw.githubusercontent.com/wiki/ufs-community/land-DA_workflow/.*",
                               r"https://github.com/ufs-community/land-DA_workflow/issues/new": 
                                 r"https://github.com/login.*",
                               r"https://doi.org/10.5281/zenodo.*": 
                                 r"https://zenodo.org/records/*",
                               r"https://doi.org/10.25923/RB19-0Q26": 
                                 r"https://repository.library.noaa.gov/view/noaa/22752",
                               r"https://doi.org/10.1016/j.physd.2006.11.008": 
                                 r"https://linkinghub.elsevier.com/retrieve/pii/S0167278906004647",
                               r"https://doi.org/.*/.*": 
                                 r"https://journals.ametsoc.org:443/view/journals/.*/.*/.*/.*",
                              }


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# The theme to use for HTML and HTML Help pages. 
html_theme = 'sphinx_rtd_theme'
html_theme_path = ["_themes", ]
html_logo= "https://github.com/ufs-community/ufs/wiki/images/ufs-epic-logo.png"

# Theme options are theme-specific and customize the look and feel of a theme
# further. 
html_theme_options = {
    "body_max_width": "none", 
    'navigation_depth': 8,
    }

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
html_context = {}

def setup(app):
    app.add_css_file('custom.css')  # may also be an URL
    app.add_css_file('theme_overrides.css')  # may also be a URL

# -- Options for intersphinx extension ---------------------------------------

intersphinx_mapping = {
   'jedi': ('https://jointcenterforsatellitedataassimilation-jedi-docs.readthedocs-hosted.com/en/1.7.0', None),
   'spack-stack': ('https://spack-stack.readthedocs.io/en/1.3.0/', None),
}

# -- Options for extlinks extension ---------------------------------------

extlinks_detect_hardcoded_links = True
extlinks = {'ccpp-techdoc': ('https://ccpp-techdoc.readthedocs.io/en/latest/%s', '%s'),
            'github': ('https://github.com/ufs-community/land-DA_workflow/%s', '%s'),
            'github-docs': ('https://docs.github.com/en/%s', '%s'),
            'gswp3': ('https://hydro.iis.u-tokyo.ac.jp/GSWP3/%s', '%s'),
            'jedi': ('https://jointcenterforsatellitedataassimilation-jedi-docs.readthedocs-hosted.com/en/8.0.0/%s', '%s'),
            'nco': ('https://www.nco.ncep.noaa.gov/idsb/implementation_standards/%s', '%s'),
            'rocoto': ('https://christopherwharrop.github.io/rocoto/%s', '%s'),
            'rst': ('https://www.sphinx-doc.org/en/master/usage/restructuredtext/%s', '%s'),
            'rtd': ('https://readthedocs.org/projects/land-da-workflow/%s', '%s'),
            'land-wflow-repo': ('https://github.com/ufs-community/land-DA_workflow/%s', '%s'),
            'land-wflow-wiki': ('https://github.com/ufs-community/land-DA_workflow/wiki/%s','%s'),
            'spack-stack': ('https://spack-stack.readthedocs.io/en/1.6.0/%s', '%s'),
            'stochphys': ('https://stochastic-physics.readthedocs.io/en/release-public-v3/%s', '%s'),
            'ufs-utils': ('https://noaa-emcufs-utils.readthedocs.io/en/latest/%s', '%s'),
            'ufs-wm': ('https://ufs-weather-model.readthedocs.io/en/develop/%s', '%s'),
            'ufs': ('https://ufs.epic.noaa.gov/%s', '%s'),
            'uw': ('https://uwtools.readthedocs.io/en/main/%s', '%s'),
            }
