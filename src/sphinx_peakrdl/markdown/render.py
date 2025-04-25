from typing import List
import os

from docutils import nodes
from docutils.utils import new_document

from .md_parsers import MD_DOCUTILS, MD_HTML

def render_to_docutils(md_string: str, src_path: str, src_line_offset: int = 0) -> List[nodes.Element]:
    MD_DOCUTILS.options["document"] = new_document(src_path)

    env = {
        "relative-images": os.path.dirname(src_path)
    }

    doc = MD_DOCUTILS.render(md_string, env)
    assert isinstance(doc, nodes.document)

    if src_line_offset != 0:
        for node in doc.traverse(nodes.Element):
            if node.line is not None:
                node.line += src_line_offset

    # MyST renderer will produce a top-level document.
    # Return the children so that they can be grafted into an existing document
    return doc.children


def render_to_html(md_string: str) -> str:
    doc = MD_HTML.render(md_string)
    return doc
