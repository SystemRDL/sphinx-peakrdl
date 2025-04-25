Using the doctree directive
===========================

.. tip::

    To view the source of this document, click the "Show Source" option under
    the GitHub menu button on this page's header.

The :rst:dir:`rdl:doctree` directive is a convenient way to insert an entire peripheral's
register map documentation into a page.

Using the directive to target the "thingamabob" component...

.. code-block:: rst

    .. rdl:doctree:: my_soc.thingamabob
        :link-to: doc

... produces the following output:

--------------------------------------------------------------------------------

.. rdl:doctree:: my_soc.thingamabob
    :link-to: doc
