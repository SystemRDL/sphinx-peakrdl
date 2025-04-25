Inline Documentation
====================

.. rst:directive:: .. rdl:docnode:: path

    Inserts the full documentation for the register model node referenced by ``path``.

    .. rubric:: Options

    .. rst:directive:option:: wrap-section:

        If set, wraps the content in a section heading.
        If this option is not specified, behavior is determined by the
        :confval:`peakrdl_doc_wrap_section` setting.

    .. rst:directive:option:: no-wrap-section:

        If set, suppresses creation of a section heading.
        If this option is not specified, behavior is determined by the
        :confval:`peakrdl_doc_wrap_section` setting.

    .. rst:directive:option:: link-to:

        Overrides the link taret preference.

        "html"
            Link to PeakRDL-HTML output
        "doc"
            Link to an inline documentation reference, if it exists.


.. rst:directive:: .. rdl:doctree:: path

    Similar to the :rst:dir:`rdl:docnode` directive, except that this will also
    generate all child docnodes recursively.

    .. rubric:: Options

    .. rst:directive:option:: link-to:

        Overrides the link taret preference.

        "html"
            Link to PeakRDL-HTML output
        "doc"
            Link to an inline documentation reference, if it exists.
