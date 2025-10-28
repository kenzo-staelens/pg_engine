.. _config_sprites:

Spritesheet Configuration
=========================

The next step in loading game data is loading images from a spritesheet, we will later be using them in :ref:`config_gameobjects` to be able to show images on the screen such that players know what's going on inside.

.. code-block:: yaml

    sprites:
      loader: SpriteLoader
      config: config/sprites.yml

.. code-block:: yaml

    sheet:
      filename: sprites/example_spritesheet.png
      width: 2
      height: 2
      colorkey: [0, 0, 0]
      rect: [0, 0, 32, 32]
      bindings:
        - red
        - green
        - blue
        - null

.. note::
   we will be using the following image as a reference to load from

   .. image:: /_static/spritesheet.png
      :alt: spritesheet image corresponging with the above configuration

With defining the example out of the way, let's start off with the spritesheet configuration and then circle back to what the registry key is for.
First is the filename/path, this is the *relative* path starting at the root passed to the :class:`~pg_engine.core.lib_abstract.TLoader` instance (here ``SpriteLoader``) and in this example points to the image above.

width, height, rect and bindings define how many images will get loaded, how big they are and where they are located in the spritesheet.

The width and height keys define the number of images that will be loaded horizontally then vertically, this spritesheet contains 2 sprites horizontally and vertically.

Rect tells the loader *where* to start loading from and how large every image in the spritesheet is. This spritesheet happens to be exactly 64x64 pixels in size, and each image in the spritesheet has a size of 32 so we are making full use of the spritesheet, though overflow is allowed.

The last of these keys, bindings, tell the loader what to call the sprites for later reference by your code. binding with a value of null, false or other falsy values get discarded.

Colorkey :py:class:`pygame.Color` defines a color which pygame can use to make parts of the loaded surface transparent.

Right now loading images will not do much for us as we are not storing the data anywhere and thus discarding everything we just loaded. In our toy example loading images of only 1024 pixels total will not cause much of a performance impact but this might not be the case for larger sprites. To solve this loaders will have access to a registry where they can store the loaded data into. here the most fitting registry would be the :term:`AssetRegistry`, which is responsible for storing surfaces (which sprites are).

.. code-block:: yaml
    :emphasize-lines: 4

    sprites:
      loader: SpriteLoader
      config: config/sprites.yml
      registry: AssetRegistry
