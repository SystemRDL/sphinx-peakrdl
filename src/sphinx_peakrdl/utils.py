from typing import Optional, List, Tuple, Union

from systemrdl.node import Node
from sphinx import version_info as sphinx_version
from docutils import nodes

if sphinx_version >= (8, 0):
    from sphinx.util.display import status_iterator, progress_message
else:
    from sphinx.util import status_iterator, progress_message


from . import design_state as DS


def lookup_rdl_node(target: str, relative_to_path: Optional[str] = None) -> Optional[Node]:

    if relative_to_path is not None:
        relative_to_node = DS.root_node.find_by_path(relative_to_path)
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
            rdl_node = DS.root_node.find_by_path(target)
        except (ValueError, IndexError):
            rdl_node = None

    return rdl_node

def wrap_paragraph(value: Union[nodes.Node, str]) -> nodes.TextElement:
    if isinstance(value, nodes.TextElement):
        # Is already wrapped in a text element
        body = value
    elif isinstance(value, nodes.Node):
        # Needs wrapping
        body = nodes.paragraph()
        body += value
    elif isinstance(value, str):
        body = nodes.paragraph(text=value)
    else:
        raise ValueError("Unhandled type", value)

    return body


class FieldList:
    def __init__(self) -> None:
        self.rows: List[Tuple[str, Union[nodes.Node, str]]] = []

    def add_row(self, name: str, value: Union[nodes.Node, str]) -> None:
        self.rows.append(
            (name, value)
        )

    def as_node(self) -> nodes.field_list:
        fl = nodes.field_list()
        for name, value in self.rows:
            f = nodes.field()
            f += nodes.field_name(text=name)

            body = wrap_paragraph(value)

            fb = nodes.field_body()
            fb += body
            f += fb

            fl += f
        return fl


class Table:
    def __init__(self, headings: List[str]) -> None:
        self.headings = headings
        self.rows = []

    def add_row(self, row: List[Union[nodes.Node, str]]) -> None:
        self.rows.append(row)

    def as_node(self) -> nodes.table:
        tgroup = nodes.tgroup(cols=len(self.headings))
        for heading in self.headings:
            tgroup += nodes.colspec()


        # Heading
        row = nodes.row()
        for heading in self.headings:
            entry = nodes.entry()
            entry += wrap_paragraph(heading)
            row += entry
        thead = nodes.thead()
        thead += row
        tgroup += thead

        # Table
        tbody = nodes.tbody()
        for row_data in self.rows:
            row = nodes.row()
            for value in row_data:
                entry = nodes.entry()
                entry += wrap_paragraph(value)
                row += entry
            tbody += row
        tgroup += tbody

        table = nodes.table()
        table += tgroup
        return table

def alpha_from_int(n: int) -> str:
    """
    Converts integers to "excel-like" alpha sequences
    """
    s = ""
    while True:
        digit_idx = n % 26
        s = chr(ord("A") + digit_idx) + s
        n = n // 26
        if n == 0:
            break
        n -= 1
    return s


__all__ = [
    "status_iterator",
    "progress_message",
    "lookup_rdl_node",
    "FieldList",
    "Table",
    "alpha_from_int",
]
