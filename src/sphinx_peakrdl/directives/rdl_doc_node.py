from typing import Sequence, Tuple, List, Optional

from sphinx.util.docutils import SphinxDirective
from sphinx.util import logging
from sphinx import addnodes
from docutils import nodes
from systemrdl.node import Node, RegNode, AddressableNode, SignalNode, RootNode
from systemrdl.rdltypes.references import PropertyReference
from systemrdl.source_ref import FileSourceRef, DetailedFileSourceRef

from ..utils import lookup_rdl_node, FieldList, Table

from .. import markdown


logger = logging.getLogger(__name__)

class RDLDocNodeDirective(SphinxDirective):
    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False

    @property
    def target(self) -> str:
        return self.arguments[0]


    def run(self) -> Sequence[nodes.Node]:
        relative_to_path: Optional[str] = self.env.ref_context.get("rdl:relative-to")
        rdl_node = lookup_rdl_node(self.target, relative_to_path)
        if rdl_node is None:
            logger.warning(
                "RDL target not found: %s",
                self.target,
                location=self.get_location(),
            )
            return []

        return self.make_rdl_node_doc(rdl_node)


    def make_rdl_node_xref(self, rdl_node: Node, text: Optional[str] = None) -> nodes.Node:
        xref = addnodes.pending_xref(
            refdoc=self.env.docname,
            refdomain="rdl",
            reftype="", # TODO: do i care about this?
            reftarget=rdl_node.get_path(),
            refwarn=False, # Don't emit a warning if can't be linked
        )
        self.set_source_info(xref)

        if text is None:
            text = rdl_node.inst_name
        xref += nodes.inline(text=text, classes=["xref"])
        return xref

    def get_desc_as_docutils(self, rdl_node: Node) -> nodes.paragraph:
        desc = rdl_node.get_property("desc") or ""

        src_ref = rdl_node.inst.property_src_ref.get("desc", rdl_node.inst.inst_src_ref)
        if isinstance(src_ref, FileSourceRef):
            path = src_ref.path
        else:
            path = "UNKNOWN"

        # TODO: Computing the line number for EVERY src ref may be time consuming
        if isinstance(src_ref, DetailedFileSourceRef):
            line = src_ref.line
        else:
            line = 0

        desc_nodes = markdown.render_to_docutils(desc, path, line)

        p = nodes.paragraph()
        p.extend(desc_nodes)
        return p


    def make_rdl_node_doc(self, rdl_node: Node) -> Sequence[nodes.Node]:
        if isinstance(rdl_node, RegNode):
            return self.make_rdl_reg_doc(rdl_node)
        elif isinstance(rdl_node, AddressableNode):
            return self.make_rdl_grouplike_doc(rdl_node)
        else:
            logger.warning(
                "Cannot generate doc content for %s components: %s",
                type(rdl_node.inst).__name__.lower(),
                self.target,
                location=self.get_location(),
            )
            return []


    def make_rdl_reg_doc(self, rdl_node: RegNode) -> Sequence[nodes.Node]:
        # TODO: Add descriptions somehow

        # Info Field List Header
        fl = FieldList()
        fl.add_row("Instance", rdl_node.inst_name)
        fl.add_row("Parent", self.make_rdl_node_xref(rdl_node.parent))
        fl.add_row("Base Offset", f"{rdl_node.raw_address_offset:#x}")
        if rdl_node.array_dimensions:
            fl.add_row("Array Dimensions", f"[{']['.join(rdl_node.array_dimensions)}]")
            fl.add_row("Array Stride", f"{rdl_node.array_stride:#x}")

        # Description
        desc_paragraph = self.get_desc_as_docutils(rdl_node)

        # Field Table
        table = Table(["Bits", "Identifier", "Access", "Reset"])
        for field in reversed(rdl_node.fields()):
            # Is actual field
            if field.width == 1:
                bitrange = f"[{field.lsb}]"
            else:
                bitrange = f"[{field.msb}:{field.lsb}]"

            access = field.get_property("sw").name
            onread = field.get_property("onread")
            onwrite = field.get_property("onwrite")
            if onread:
                access += f", {onread.name}"
            if onwrite:
                access += f", {onwrite.name}"

            reset_value = field.get_property("reset")
            if reset_value is None:
                reset = "-"
            elif isinstance(reset_value, int):
                reset = f"{reset_value:#x}"
            elif isinstance(reset_value, PropertyReference):
                reset = self.make_rdl_node_xref(reset_value.node) + "->" + reset_value.name
            elif isinstance(reset_value, SignalNode):
                reset = reset_value.get_path()
            else:
                reset = self.make_rdl_node_xref(reset_value)

            table.add_row([
                bitrange,
                field.inst_name,
                access,
                reset,
            ])

        # Field descriptions
        def_list = nodes.definition_list()
        for field in reversed(rdl_node.fields()):
            desc = field.get_property("desc")
            if not desc:
                continue

            dli = nodes.definition_list_item()
            def_list.append(dli)

            dl_term = nodes.term(text = field.inst_name)
            dl_def = nodes.definition()
            dl_def_p = self.get_desc_as_docutils(field)
            dl_def.append(dl_def_p)

            dli.append(dl_term)
            dli.append(dl_def)



        return [fl.as_node(), desc_paragraph, table.as_node(), def_list]


    def make_rdl_grouplike_doc(self, rdl_node: AddressableNode) -> Sequence[nodes.Node]:
        # Info Field List Header
        fl = FieldList()
        fl.add_row("Instance", rdl_node.inst_name)
        if not isinstance(rdl_node.parent, RootNode):
            fl.add_row("Parent", self.make_rdl_node_xref(rdl_node.parent))
            fl.add_row("Base Offset", f"{rdl_node.raw_address_offset:#x}")
        if rdl_node.array_dimensions:
            # FIXME: cant join ints: fl.add_row("Array Dimensions", f"[{']['.join(rdl_node.array_dimensions)}]")
            fl.add_row("Array Stride", f"{rdl_node.array_stride:#x}")

        # Description
        desc_paragraph = self.get_desc_as_docutils(rdl_node)

        # Child table
        table = Table(["Offset", "Identifier"])
        for child in rdl_node.children():
            if not isinstance(child, AddressableNode):
                continue

            offset = f"{child.raw_address_offset:#x}"

            if child.array_dimensions:
                # FIXME: cant join ints: text = child.inst_name + f"[{']['.join(child.array_dimensions)}]"
                text = child.inst_name
                identifier = self.make_rdl_node_xref(child, text)
            else:
                identifier = self.make_rdl_node_xref(child)

            table.add_row([
                offset,
                identifier,
            ])

        return [fl.as_node(), desc_paragraph, table.as_node()]
