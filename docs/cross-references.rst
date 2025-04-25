Cross-references
================

.. role:: code-rst(code)
   :language: reStructuredText

.. rst:directive:: .. rdl:relative-to:: path

    It can be cumbersome to always specify the full register hierarchy in your docs.
    This directive lets you temporarily set a more localized scope to a hierarchy
    to make following references in the same document easier to manage.

    .. code-block:: rst

        Annoying! :rdl:ref:`very.long.path.to.my_block.my_register`

        .. rdl:relative-to:: very.long.path.to

        Much better! :rdl:ref:`my_block.my_register`


    Cross-references will first search relative to the path specified, then
    fall back to searching the absolute path.





.. rst:role:: rdl:ref

    Insert an inline cross-reference link to an existing register reference node.

    The contents of the link text can be controlled in several ways:

    * :code-rst:`:rdl:ref:\`path.to.my_block.my_register\`` Results in the full link text: ``path.to.my_block.my_register``
    * :code-rst:`:rdl:ref:\`~path.to.my_block.my_register\`` Truncates text to only show the last segment: ``my_register``
    * :code-rst:`:rdl:ref:\`path.to.|my_block.my_register\`` Truncates everything before the ``|``: ``my_block.my_register``
    * :code-rst:`:rdl:ref:\`My Awesome Register <path.to.my_block.my_register>\`` displays custom text: ``My Awesome Register``

    Whether the link points to PeakRDL-HTML reference, or an inline :rst:dir:`rdl:docnode`
    depends on the :confval:`peakrdl_default_link_to` setting.


.. rst:role:: rdl:html-ref

    Same as the :rst:role:`rdl:ref` role, except this will prefer linking to
    PeakRDL-HTML reference, regardless of the :confval:`peakrdl_default_link_to` setting.

.. rst:role:: rdl:doc-ref

    Same as the :rst:role:`rdl:ref` role, except this will prefer linking to
    an inline :rst:dir:`docnode`, regardless of the :confval:`peakrdl_default_link_to` setting.
