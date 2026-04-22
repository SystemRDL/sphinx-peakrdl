from pathlib import Path
from typing import TYPE_CHECKING

from .__about__ import __version__
from . import config
from . import build
from . import html
from .domain import PeakRDLDomain

if TYPE_CHECKING:
    from sphinx.application import Sphinx
    from sphinx.util.typing import ExtensionMetadata


def _setup_static_path(app: "Sphinx") -> None:
    static_dir = str(Path(__file__).parent / "_static")
    if static_dir not in app.config.html_static_path:
        app.config.html_static_path.append(static_dir)


def setup(app: "Sphinx") -> "ExtensionMetadata":
    config.setup_config(app)

    app.connect("config-inited", config.elaborate_config_callback)
    app.connect("env-before-read-docs", build.compile_input_callback)
    app.connect("html-collect-pages", html.write_html_callback)
    app.connect("builder-inited", _setup_static_path)

    app.add_domain(PeakRDLDomain)
    app.add_css_file("peakrdl.css")

    return {
        'version': __version__,
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
