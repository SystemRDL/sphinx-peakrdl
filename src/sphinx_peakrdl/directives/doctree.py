from typing import Sequence, Optional

from docutils import nodes

from sphinx.util import logging

from systemrdl.node import Node, AddressableNode

from .docnode import RDLDocNodeDirective, link_to_option
from ..utils import lookup_rdl_node

logger = logging.getLogger(__name__)

class RDLDocTreeDirective(RDLDocNodeDirective):

    option_spec = {
        "link-to": link_to_option,
        # TODO: option for top to have heading or not
        # TODO: option to skip top
    }

    def run(self) -> Sequence[nodes.Node]:
        # Try to lookup node
        relative_to_path: Optional[str] = self.env.ref_context.get("rdl:relative-to")
        rdl_node = lookup_rdl_node(self.target, relative_to_path)
        if rdl_node is None:
            logger.warning(
                "RDL target not found: %s",
                self.target,
                location=self.get_location(),
            )
            return []

        # Always add headings
        self.options["wrap-section"] = True

        return [self.make_rdl_node_doctree(rdl_node)]


    def make_rdl_node_doctree(self, rdl_node: Node) -> nodes.Element:
        result = self.make_rdl_node_doc(rdl_node)

        # result is guaranteed to be 1 element that is the <section> node
        # due to wrap-section forced to True
        assert len(result) == 1
        content = result[0]

        for child in rdl_node.children():
            if not isinstance(child, AddressableNode):
                break

            child_content = self.make_rdl_node_doctree(child)
            content += child_content

        return content
