from typing import TYPE_CHECKING
import os

from peakrdl_html import HTMLExporter

from . import design_state as DS
from .utils import progress_message

if TYPE_CHECKING:
    from sphinx.application import Sphinx

HTML_ROOT = "peakrdl-html"
HTML_INDEX = HTML_ROOT + "/index"


def write_html_callback(app: "Sphinx") -> None:
    """
    Called by the 'html-collect-pages' event.

    Export HTML
    """
    if DS.top_node is None:
        return []

    e = HTMLExporter(
        extra_doc_properties=app.config.peakrdl_extra_doc_properties
    )

    if app.config.peakrdl_title is None:
        title = f"{DS.top_node.inst_name} Register Reference"
    else:
        title = app.config.peakrdl_title

    with progress_message("Writing PeakRDL HTML"):
        e.export(
            DS.top_node,
            os.path.join(app.builder.outdir, HTML_ROOT),
            title=title,
            home_url=app.builder.get_relative_uri(HTML_INDEX, app.config.root_doc)
        )

    return []
