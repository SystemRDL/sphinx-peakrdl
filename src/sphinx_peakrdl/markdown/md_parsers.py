from typing import TYPE_CHECKING, Callable

from markdown_it.renderer import RendererProtocol, RendererHTML

from mdit_py_plugins.admon import admon_plugin
from mdit_py_plugins.dollarmath import dollarmath_plugin

from myst_parser.config.main import MdParserConfig
from myst_parser.parsers.mdit import create_md_parser

from .docutils_renderer import PeakRDLDocutilsRenderer

if TYPE_CHECKING:
    from markdown_it import MarkdownIt

def _get_md_parser(renderer: Callable[["MarkdownIt"], RendererProtocol]) -> "MarkdownIt":
    config = MdParserConfig()

    # Use MyST utility function to bootstrap creation of the markdown parser
    # Start with a pure CommonMark implementation, without any MyST extensions
    config.commonmark_only = True
    md = create_md_parser(config, renderer)

    # Enable extensions to match the prior python-markdown extension as much as possible
    md.enable([
        "table",
        "linkify",
    ])

    # Enables !!!-style admonitions
    md.use(admon_plugin)

    # Enables inline $...$ and block $$...$$ math tags
    md.use(
        dollarmath_plugin,
        allow_labels=False,
    )

    return md

MD_DOCUTILS = _get_md_parser(PeakRDLDocutilsRenderer)
MD_HTML = _get_md_parser(RendererHTML)
