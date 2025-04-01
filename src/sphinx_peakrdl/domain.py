from typing import TYPE_CHECKING, Optional

from docutils.nodes import Element
from sphinx.domains import Domain
from sphinx.util import logging
from docutils import nodes
from systemrdl.node import Node as RDLNode
from systemrdl.node import FieldNode

from .roles import xrefs
from .directives import relative_to
from . import design_state as DS
from .html import HTML_INDEX

logger = logging.getLogger(__name__)

class PeakRDLDomain(Domain):
    name = "rdl"
    label = "PeakRDL"
    roles = {
        "ref": xrefs.RDLRefRole(),
        "html-ref": xrefs.RDLHTMLRefRole(),
        "doc-ref": xrefs.RDLDocRefRole(),
    }
    directives = {
        "relative-to": relative_to.RDLRelativeTo,
    }

    def resolve_xref(self, env, fromdocname, builder, typ, target, node, contnode) -> Optional[Element]:
        """
        Resolve RDL references.
        """
        # Re-resolve relative-to
        relative_to_path: Optional[str] = node.get("rdl:relative-to")
        if relative_to_path is not None:
            relative_to_node = DS.top_node.find_by_path(relative_to_path)
        else:
            relative_to_node = None

        # Try relative search first, if set
        rdl_node = None
        if relative_to_node:
            try:
                rdl_node = relative_to_node.find_by_path(target)
            except (ValueError, IndexError):
                rdl_node = None

        # Fall back to global scope
        if rdl_node is None:
            try:
                rdl_node = DS.top_node.find_by_path(target)
            except (ValueError, IndexError):
                rdl_node = None

        # Did it find it?
        if rdl_node is None:
            logger.warning(
                "RDL target not found: %s",
                target,
                location=node,
            )
            return None

        # Build link
        XXX = node.get("rdl:target-type")
        return self.make_html_refnode(builder, fromdocname, contnode, rdl_node)

    def make_html_refnode(self, builder, fromdocname, contnode, rdl_node: RDLNode) -> nodes.reference:
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
