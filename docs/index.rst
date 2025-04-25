Introduction
============

``sphinx-peakrdl`` is an extension that integrates PeakRDL's register map
documentation capabilities into your `Sphinx-Doc <https://www.sphinx-doc.org/en/master/index.html>`_
project.

Using this extension, you can:

* Automatically generate PeakRDL-HTML output from within the Sphinx build flow
* Create cross-reference links to register map elements from your reStructuredText document.
* Insert register reference content inline into your document (Useful if you want to generate offline PDF docs)

Get Started
-----------

TODO: Add disclaimer banner to docs - help wanted!

Install
~~~~~~~
Install from `PyPi`_ using pip

.. code-block:: bash

    python3 -m pip install sphinx-peakrdl

.. _PyPi: https://pypi.org/project/sphinx-peakrdl



Configure
~~~~~~~~~
Enable the extension in your Sphinx-Doc ``conf.py``:

.. code-block:: python
    :caption: conf.py

    extensions = [
        "sphinx_peakrdl",
    ]

Provide the extension a list of PeakRDL input files to process:

.. code-block:: python
    :caption: conf.py

    peakrdl_input_files = [
        "path/to/turboencabulator.rdl",
        "path/to/ethernet_mac.rdl",
        "path/to/thingamabob_top.rdl",
    ]


Start cross-referencing!
~~~~~~~~~~~~~~~~~~~~~~~~
Cross-reference your documentation to automatically-generated PeakRDL-HTML pages.

This really useful when writing software guides or other reference pages. For example:

.. code-block:: rst

    Thingamabob startup sequence:

    1. Configure the :rdl:ref:`my_soc.thingamabob.ctrl` register to the desired settings.
    2. Enable the device by setting :rdl:ref:`my_soc.thingamabob.ctrl.en` to ``1``.
    3. Check :rdl:ref:`my_soc.thingamabob.status` for errors.

Results in the following output:

    Thingamabob startup sequence:

    1. Configure the :rdl:ref:`my_soc.thingamabob.ctrl` register to the desired settings.
    2. Enable the device by setting :rdl:ref:`my_soc.thingamabob.ctrl.en` to ``1``.
    3. Check :rdl:ref:`my_soc.thingamabob.status` for errors.



Links
-----

- `Source repository <https://github.com/SystemRDL/sphinx-peakrdl>`_
- `Release Notes <https://github.com/SystemRDL/sphinx-peakrdl/releases>`_
- `Issue tracker <https://github.com/SystemRDL/sphinx-peakrdl/issues>`_
- `PyPi <https://pypi.org/project/sphinx-peakrdl>`_



.. toctree::
    :hidden:

    self
    cross-references
    inline-documentation
    configuring


.. toctree::
    :hidden:
    :caption: Examples

    examples/xrefs.rst
    examples/docnode.rst
    examples/doctree.rst
