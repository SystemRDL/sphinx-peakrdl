from typing import Optional

from docutils.nodes import Element
from sphinx.domains import Domain
from sphinx.util import logging
from docutils import nodes
from systemrdl.node import Node, FieldNode

from .roles import xrefs
from .directives.relative_to import RDLRelativeToDirective
from .directives.docnode import RDLDocNodeDirective
from .directives.doctree import RDLDocTreeDirective
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
        "docnode": RDLDocNodeDirective,
        "doctree": RDLDocTreeDirective,
    }

    initial_data = {
        # rdl_path --> docname
        "rdl_docnodes": {}
    }

    def html_is_available(self, builder_name: str) -> bool:
        """
        Whether PeakRDL-html output is available.
        This could either be because the html sphinx builder is not being used,
        or because HTML output was disabled in the config
        """
        if self.env.config.peakrdl_html_enable is False:
            return False

        if builder_name in {"html", "dirhtml"}:
            return True
        return False

    def resolve_xref(self, env, fromdocname, builder, typ, target, node, contnode) -> Optional[Element]:
        """
        Resolve RDL references.
        """
        relative_to_path: Optional[str] = node.get("rdl:relative-to")
        rdl_node = lookup_rdl_node(target, relative_to_path)

        if rdl_node is None:
            return None

        # Build link
        target_type: str = node.get("rdl:target-type", self.env.config.peakrdl_default_link_to)

        if target_type == "html":
            # User prefers a link to PeakRDL-html output
            if self.html_is_available(builder.name):
                return self.make_html_refnode(builder, fromdocname, contnode, rdl_node)
            else:
                return self.make_docnode_refnode(builder, fromdocname, contnode, rdl_node)
        elif target_type == "doc":
            # User prefers a link to internal doc
            result = self.make_docnode_refnode(builder, fromdocname, contnode, rdl_node)
            if result is not None:
                return result

            # No docnode available to link to.
            # Fall back to html if available
            if self.html_is_available(builder.name):
                return self.make_html_refnode(builder, fromdocname, contnode, rdl_node)
            else:
                return None


    def make_html_refnode(self, builder, fromdocname, contnode, rdl_node: Node) -> nodes.reference:

        if isinstance(rdl_node, FieldNode):
            # Target is a field.
            # For HTML, fields are a specific id of a reg page
            targetid = rdl_node.inst_name
            rdl_node = rdl_node.parent
        else:
            targetid = None

        path = rdl_node.get_path(empty_array_suffix="")
        uri = builder.get_relative_uri(fromdocname, HTML_INDEX)

        node = nodes.reference('', '', internal=True)
        if targetid:
            node['refuri'] = uri + f"?p={path}#{targetid}"
        else:
            node['refuri'] = uri + f"?p={path}"

        node += contnode
        return node

    def make_docnode_refnode(self, builder, fromdocname, contnode, rdl_node: Node) -> Optional[nodes.reference]:
        ref_id = rdl_node.get_path(array_suffix="", empty_array_suffix="")

        ref_docname: Optional[str] = self.data["rdl_docnodes"].get(ref_id)
        if ref_docname is None:
            # No docnode to link to. Give up
            return None

        uri = builder.get_relative_uri(fromdocname, ref_docname)
        node = nodes.reference('', '', internal=True)
        node['refuri'] = uri + f"#{ref_id}"

        node += contnode
        return node
