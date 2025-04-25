from typing import TYPE_CHECKING

from docutils import nodes

from myst_parser.mdit_to_docutils.base import DocutilsRenderer

if TYPE_CHECKING:
    from markdown_it.tree import SyntaxTreeNode

class PeakRDLDocutilsRenderer(DocutilsRenderer):
    """
    MyST Docutils renderer that adds support for features not covered by the
    original renderer:

    * Admonitions via ``mdit_py_plugins.admon``
    """

    def render_admonition(self, token: "SyntaxTreeNode") -> None:
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

    def render_admonition_title(self, token: "SyntaxTreeNode") -> None:
        """
        No-op. Discard this node
        """
