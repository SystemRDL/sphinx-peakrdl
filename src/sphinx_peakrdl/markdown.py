from typing import Callable, List
import os

from markdown_it import MarkdownIt
from markdown_it.renderer import RendererProtocol
from markdown_it.renderer import RendererHTML
from markdown_it.tree import SyntaxTreeNode

from myst_parser.config.main import MdParserConfig
from myst_parser.parsers.mdit import create_md_parser
from myst_parser.mdit_to_docutils.base import DocutilsRenderer

from mdit_py_plugins.admon import admon_plugin

from docutils import nodes
from docutils.utils import new_document

def _get_md_parser(renderer: Callable[[MarkdownIt], RendererProtocol]) -> MarkdownIt:
    config = MdParserConfig()
    config.commonmark_only = True # Start without any myst extensions
    md = create_md_parser(config, renderer)
    md.enable([
        "table",
        "linkify",
    ])
    md.use(admon_plugin)

    return md


class PeakRDLDocutilsRenderer(DocutilsRenderer):
    def render_admonition(self, token: SyntaxTreeNode) -> None:
        """
        Render admonitions provided by the 'mdit_py_plugins.admon' plugin and convert them to
        docutils nodes.

        This callback is implicitly called when it encounters a SyntaxTreeNode
        whose .type == "admonition"

        The provided node has the following children:
            token.children[0]
                .type = admonition_title
                This can be discarded. Does not provide any meaningful structure

            token.children[1+]
                All other children represent the body of the admonition

        """
        # Get the admonition title
        title: str = token.meta["tag"]
        title = title.capitalize()

        # Create a docutils admonition node
        admonition_node = nodes.admonition()
        title_node = nodes.title(text=title)
        admonition_node.append(title_node)
        admonition_node['classes'].append('admonition-' + nodes.make_id(title))
        self.copy_attributes(token, admonition_node, keys=("class", "id", "start"))
        self.add_line_and_source_path(admonition_node, token)

        # Process children
        with self.current_node_context(admonition_node, append=True):
            self.render_children(token)

    def render_admonition_title(self, token: SyntaxTreeNode) -> None:
        """
        No-op. Discard this node
        """
        pass



MD_DOCUTILS = _get_md_parser(PeakRDLDocutilsRenderer)
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


MD_HTML = _get_md_parser(RendererHTML)
def render_to_html(md_string: str) -> str:
    doc = MD_HTML.render(md_string)
    return doc
