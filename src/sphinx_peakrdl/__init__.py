from typing import TYPE_CHECKING

from .__about__ import __version__
from . import config
from . import build
from . import html
from .domain import PeakRDLDomain

if TYPE_CHECKING:
    from sphinx.application import Sphinx
    from sphinx.util.typing import ExtensionMetadata

def setup(app: "Sphinx") -> "ExtensionMetadata":
    config.setup_config(app)

    app.connect("config-inited", config.elaborate_config_callback)
    app.connect("env-before-read-docs", build.compile_input_callback)
    app.connect("html-collect-pages", html.write_html_callback)

    app.add_domain(PeakRDLDomain)

    return {
        'version': __version__,
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
