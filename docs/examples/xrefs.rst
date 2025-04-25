Using Cross-references
======================

.. tip::

    To view the source of this document, click the "Show Source" option under
    the GitHub menu button on this page's header.

Cross-references are a powerful way to embed links to your register reference
anywhere in your documentation.

Basic cross-references
----------------------

Here is a basic example of some cross-references:

    1. Configure the :rdl:ref:`my_soc.thingamabob.ctrl` register to the desired settings.
    2. Enable the device by setting :rdl:ref:`my_soc.thingamabob.ctrl.en` to ``1``.
    3. Check :rdl:ref:`my_soc.thingamabob.status` for errors.


Using relative paths
--------------------

If your document is focusing on details for a particular component, it can be cumbersome to type out the entire path each time.

Here is the same example again, but without needing to specify the full path every time:

    .. rdl:relative-to:: my_soc.thingamabob

    1. Configure the :rdl:ref:`ctrl` register to the desired settings.
    2. Enable the device by setting :rdl:ref:`ctrl.en` to ``1``.
    3. Check :rdl:ref:`status` for errors.


Control link text
-----------------
By default, a link's text will match the text used in the cross-reference.
    The contents of the link text can be controlled in several ways:

    * :code-rst:`:rdl:ref:\`my_soc.turboencabulator.grammeter\`` Results in the full link text:

      :rdl:ref:`my_soc.turboencabulator.grammeter`

    * :code-rst:`:rdl:ref:\`~my_soc.turboencabulator.grammeter\`` Truncates text to only show the last segment:

      :rdl:ref:`~my_soc.turboencabulator.grammeter`

    * :code-rst:`:rdl:ref:\`my_soc.|turboencabulator.grammeter\`` Truncates everything before the ``|``:

      :rdl:ref:`my_soc.|turboencabulator.grammeter`

    * :code-rst:`:rdl:ref:\`The Amazing Grammeter <my_soc.turboencabulator.grammeter>\`` displays custom text:

      :rdl:ref:`The Amazing Grammeter <my_soc.turboencabulator.grammeter>`



Controlling where a link takes you
----------------------------------

The :rst:role:`rdl:html-ref` and :rst:role:`rdl:doc-ref` roles can be used to
explicitly choose which documentation target the link will point to.

* Using :rst:role:`rdl:ref` links to the HTML output by default: :rdl:ref:`my_soc.thingamabob.status`
* Using :rst:role:`rdl:doc-ref` will prefer linking to the inline docs, if they exist: :rdl:doc-ref:`my_soc.thingamabob.status`
