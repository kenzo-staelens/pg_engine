.. PG_Engine documentation master file, created by
   sphinx-quickstart on Wed Oct 22 16:37:09 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to PG_Engine's documentation!
=====================================

PG_Engine is a module to build pygame games in an ECS system much like Unity, Unreal Engine or other popular game engines through more configuration than actual code. Nearly all internals of the engine are replaceable or extensible by custom code if you would wish to do so. As is defining custom components if what is provided is lacking in functionality.

Installation
------------

Due to installation conflicts when installing one of `pygame <https://www.pygame.org/>`_ or `pygame-ce <https://pyga.me/>`_ installing either as an optional dependency is required if neither is available on your system.

.. code-block:: bash

   pip install pg-ecs-engine[pygame] -U
   pip install pg-ecs-engine[pygame-ce] -U

Or from source

.. code-block:: bash

   pip install .[pygame] -U
   pip install .[pygame-ce] -U

.. note::

  The quickstart guide (mentioned below) makes use of pygame-gui and will require pygame-ce over pygame. Make sure to uninstall your local version of pygame before installing pygame-ce. It can be installed with

  .. code-block:: bash

    pip install pg-ecs-engine[gui] -U

Why is it called ``pg-ecs-engine``? Blame PyPi.

Source code on Github
---------------------

The source code for PG_Engine is `available on Github here <https://github.com/kenzo-staelens/pg_engine>`_

Getting Started
---------------

Go to our :ref:`quickstart` to set up your first project. Even though this module puts a large abstraction layer on top of pygame it is still recommended to have a basic understanding of how to use the underlying library. whether that's pygame or pygame-ce matters little as this library supports both.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   quickstart
   terms
   api

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
