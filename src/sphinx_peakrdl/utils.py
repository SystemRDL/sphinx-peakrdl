from sphinx import version_info as sphinx_version

if sphinx_version >= (8, 0):
    from sphinx.util.display import status_iterator, progress_message
else:
    from sphinx.util import status_iterator, progress_message

__all__ = [
    "status_iterator",
    "progress_message",
]
