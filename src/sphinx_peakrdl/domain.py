from typing import TYPE_CHECKING, Optional

from docutils.nodes import Element
from sphinx.domains import Domain
from sphinx.util import logging
from docutils import nodes
from systemrdl.node import Node, FieldNode

from .roles import xrefs
from .directives.relative_to import RDLRelativeToDirective
from .directives.rdl_doc_node import RDLDocNodeDirective
from .html import HTML_INDEX
from .utils import lookup_rdl_node

logger = logging.getLogger(__name__)

class PeakRDLDomain(Domain):
    name = "rdl"
    label = "PeakRDL"
    roles = {
        "ref": xrefs.RDLRefRole(warn_dangling=True),
        "html-ref": xrefs.RDLHTMLRefRole(warn_dangling=True),
        "doc-ref": xrefs.RDLDocRefRole(warn_dangling=True),
    }
    directives = {
        "relative-to": RDLRelativeToDirective,
        "node": RDLDocNodeDirective,
    }


    def resolve_xref(self, env, fromdocname, builder, typ, target, node, contnode) -> Optional[Element]:
        """
        Resolve RDL references.
        """
        relative_to_path: Optional[str] = node.get("rdl:relative-to")
        rdl_node = lookup_rdl_node(target, relative_to_path)

        if rdl_node is None:
            return None

        # Build link
        XXX = node.get("rdl:target-type")
        return self.make_html_refnode(builder, fromdocname, contnode, rdl_node)


    def make_html_refnode(self, builder, fromdocname, contnode, rdl_node: Node) -> nodes.reference:
        node = nodes.reference('', '', internal=True)

        if isinstance(rdl_node, FieldNode):
            # Target is a field.
            # For HTML, fields are a specific id of a reg page
            targetid = rdl_node.inst_name
            rdl_node = rdl_node.parent
        else:
            targetid = None

        path = rdl_node.get_path()
        uri = builder.get_relative_uri(fromdocname, HTML_INDEX)

        if targetid:
            node['refuri'] = uri + f"?p={path}#{targetid}"
        else:
            node['refuri'] = uri + f"?p={path}"

        node += contnode
        return node
