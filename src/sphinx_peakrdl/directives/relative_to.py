from typing import TYPE_CHECKING, List

from sphinx.util.docutils import SphinxDirective
from sphinx.util import logging

from .. import design_state as DS

if TYPE_CHECKING:
    from docutils.nodes import Node

logger = logging.getLogger(__name__)

class RDLRelativeTo(SphinxDirective):
    """
    This directive sets the relative search scope of an RDL node
    """

    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False

    def run(self) -> List["Node"]:
        path = self.arguments[0].strip()
        if path == "None":
            path = None

        # Validate that the path exists
        if DS.top_node is None:
            return []
        try:
            node = DS.top_node.find_by_path(path)
        except (ValueError, IndexError):
            node = None

        if node is None:
            location = self.state_machine.get_source_and_line(self.lineno)
            logger.warning(
                "RDL target not found: %s", path,
                location=location
            )
            return []

        self.env.ref_context["rdl:relative-to"] = path
        return []
