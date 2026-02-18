"""Register to WaveDrom JSON conversion.

Works directly with systemrdl-compiler RegNode/FieldNode — no additional
dependencies beyond systemrdl-compiler itself.
"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from systemrdl.rdltypes import AccessType

if TYPE_CHECKING:
    from systemrdl.node import FieldNode, RegNode


def register_to_wavedrom(rdl_node: RegNode) -> dict:
    """Convert a RegNode to a WaveDrom bitfield JSON dict.

    Returns a dict ready for ``json.dumps()``, in the format
    ``{"reg": [...], "config": {"lanes": N, ...}}``.

    Fields and gaps are emitted LSB-first (bit 0 = first element),
    which matches WaveDrom's bit numbering convention.
    """
    regwidth = rdl_node.get_property("regwidth")
    accesswidth = rdl_node.get_property("accesswidth")

    # Sort fields by lsb ascending (LSB-first for WaveDrom)
    fields = sorted(rdl_node.fields(), key=lambda f: f.lsb)

    # Single-pass: walk fields LSB-first, emitting gap entries for holes
    reg_entries: list[dict] = []
    pos = 0
    for field in fields:
        if field.lsb > pos:
            # Gap between current position and this field
            reg_entries.append(_gap_entry(field.lsb - pos))
        reg_entries.append(_field_entry(field))
        pos = field.msb + 1

    # Trailing gap to fill out the register width
    if pos < regwidth:
        reg_entries.append(_gap_entry(regwidth - pos))

    # Compute vspace for rotated labels on narrow fields
    max_rotated_len = max(
        (len(f.inst_name) for f in fields if f.width <= 2), default=0
    )
    vspace = max(80, max_rotated_len * 8 + 80) if max_rotated_len else 80

    lanes = regwidth // accesswidth
    config: dict = {"lanes": lanes, "hspace": 888, "vspace": vspace}

    return {"reg": reg_entries, "config": config}


def _field_entry(field: FieldNode) -> dict:
    """Convert a single FieldNode to a WaveDrom reg entry."""
    sw = field.get_property("sw")
    access_str = _access_to_str(sw)
    entry: dict = {
        "name": field.inst_name,
        "bits": field.width,
        "attr": [access_str],
        "type": _access_to_type(sw),
    }
    if field.width <= 2:
        entry["rotate"] = -90
    return entry


def _gap_entry(width: int) -> dict:
    """Create a WaveDrom reserved/gap entry."""
    return {"bits": width, "name": "", "type": 5}


def _access_to_str(sw: AccessType) -> str:
    """Map AccessType to a short display string."""
    return {
        AccessType.rw: "rw",
        AccessType.r: "ro",
        AccessType.w: "wo",
        AccessType.rw1: "rw1",
        AccessType.w1: "w1",
        AccessType.na: "na",
    }.get(sw, "?")


def _access_to_type(sw: AccessType) -> int:
    """Map AccessType to WaveDrom type (colour index)."""
    return {
        AccessType.rw: 0,
        AccessType.r: 2,
        AccessType.w: 4,
        AccessType.rw1: 0,
        AccessType.w1: 4,
        AccessType.na: 5,
    }.get(sw, 0)
