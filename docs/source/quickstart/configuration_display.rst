.. _config_display:

Display Configuration
=====================

The display configuration, albeit small, is used to configure engine components that handle rendering and other user interractions like :class:`~pg_engine.core.bases.lib_abstract.TRenderer` and :class:`~pg_engine.core.bases.lib_abstract.TUIManager`. It is also the first file in this quickstart guide that uses a reference file for it's data.

.. code-block:: yaml
   :emphasize-lines: 3,4

   display:
     loader: YamlLoader
     loader_args:
       useref: config/ref.yml
     config: config/display.yml
     processor: GraphicsProcessor


.. code-block:: yaml
   :emphasize-lines: 3,5

   renderer:
     display_mode:
       size: *display_size
   uimanager:
     window_resolution: *display_size

Loaders subclassing from :class:`~pg_engine.core.loaders.YamlLoader` are able to load anchors from another file without requiring to include that file's content into the loaded configuration file. Such reference files can be useful for storing constants several other files such that you don't have to edit multiple files when only one value changes.

.. code-block:: yaml
   :emphasize-lines: 1

    display_size: &display_size
      - 400
      - 400

In this example we are using the reference data to set the size of both our renderer and uimanager's sizes to a 400 by 400 pixel square which we can easily change without accidentally forgetting to update the other. In our Root configuration file we are using ``GraphicsProcessor`` to apply these settings on our renderer and uimanager instances without the loader having to know how or what instances must be configured as *it's* job is to only load the data in a usable form.