"""
Helper module to store build-time information.

This is used instead of the Sphinx BuildEnvironment because it is not useful
for this data to be pickled and retained across builds.
Hate global variables? Me too, but I think we'll be fine this one time.
"""

from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from argparse import Namespace

    from peakrdl.config.loader import AppConfig
    from peakrdl.plugins.importer import ImporterPlugin
    from systemrdl.node import AddrmapNode


# PeakRDL Config TOML data
peakrdl_cfg: "AppConfig"

# List of importer plugins
importers: List["ImporterPlugin"]

# Dummy argparse namespace preloaded with importer args
# This is a hack to satisfy calling requirements of importer plugins
argparse_options: "Namespace"

top_node: Optional["AddrmapNode"] = None
