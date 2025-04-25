Using the docnode directive
===========================

.. tip::

    To view the source of this document, click the "Show Source" option under
    the GitHub menu button on this page's header.

The :rst:dir:`rdl:docnode` directive can be used to insert the content of a
single register model node into a document.

For example, one could insert the reference for the top-level SoC address layout using ...

.. code-block:: rst

    .. rdl:docnode:: my_soc
        :link-to: doc

... which produces the following output:

--------------------------------------------------------------------------------

.. rdl:docnode:: my_soc
