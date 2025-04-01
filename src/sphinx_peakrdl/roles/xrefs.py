from typing import Tuple

from sphinx.roles import XRefRole

class RDLRefRole(XRefRole):
    """
    cross-reference to an RDL node.

    Automatically resolves whether it links to the PeakRDL-HTML output vs inline
    doc content based on which builder is used, as well as config settings
    """
    def process_link(self, env, refnode, has_explicit_title, title, target) -> Tuple[str, str]:
        # Copy relevant context about the reference
        refnode["rdl:relative-to"] = env.ref_context.get("rdl:relative-to")

        if not has_explicit_title:
            # target is title. Format it accordingly
            title = target
            if title.startswith("~"):
                # First character is tilde. Only show the leaf node in the title
                title = title.lstrip("~")
                didx = title.rfind(".")
                if didx != -1:
                    title = title[didx + 1:]

        target = target.lstrip("~")

        return title, target

class RDLHTMLRefRole(RDLRefRole):
    """
    RDL cross-reference that explicitly links to the HTML reference
    """
    def process_link(self, env, refnode, has_explicit_title, title, target) -> Tuple[str, str]:
        refnode["rdl:target-type"] = "html"
        return super().process_link(env, refnode, has_explicit_title, title, target)


class RDLDocRefRole(RDLRefRole):
    """
    RDL cross-reference that explicitly links to the node's reference emitted within the doc
    """
    def process_link(self, env, refnode, has_explicit_title, title, target) -> Tuple[str, str]:
        refnode["rdl:target-type"] = "doc"
        return super().process_link(env, refnode, has_explicit_title, title, target)
