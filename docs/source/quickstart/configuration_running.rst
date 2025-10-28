.. _configuration_running:

Running your game
=================

Given the fairly extensive configuration done before this point, it makes it now makes it fairly trivial to run your game from a single configuration file.

A first step in starting the game is, just like you would with pygame is calling init of PG_Engine, it will handle the registration of all built in or otherwise provided engine parts, gameobject components and other code that may need registration as well as calling ``pygame.init()``.

.. code-block:: python

    import pg_engine

    pg_engine.init()

Next is loading your game's configuration into memory and building up a gameinstance in a state before the gameloop starts running. here  :class:`~pg_engine.core.loaders.game_config_loader.GameConfigLoader` will be orchestrating the loading of all engine parts and game components as well as creating instances where necessary.

.. code-block:: python
   :emphasize-lines: 2,3,7,9,10,11,12

   import pg_engine
   from pg_engine.core import GameConfigLoader
   import pathlib

   pg_engine.init()

   config_root = pathlib.Path(__file__).parent

   GameConfigLoader(
       filename='config/config.yml',
       root=config_root,
   ).load()

Last we just need to start the game.

.. code-block:: python
   :emphasize-lines: 2,12,13

   import pg_engine
   from pg_engine.core import GameConfigLoader, TGame

   pg_engine.init()

   config_root = pathlib.Path(__file__).parent

   GameConfigLoader(
       filename='config/config.yml',
       root=config_root,
   ).load()
   TGame().run()
   pg_engine.quit()  # cleaning up like responsible developers


If your IDE has a type checker active it may complain that :class:`~pg_engine.core.bases.lib_abstract.TGame` is an abstract class. Under normal circumstances an abstract class cannot be instantiated.
   
Instead ``TGame()`` stands in a proxy for the game instance type you defined in :ref:`config_gameinstance` (we used :class:`~pg_engine.core.bases.base_game.BaseGame` in this tutorial). This is possible due to the singleton nature of ``TGame`` which lets it skip normal instantiation in favor of an existing instance.

.. hint::

   If you prefer using literal Singleton access the following code is also valid, though PG_Engine liberally makes use of the version above.

   .. code-block:: python

      from pg_engine.core.bases import TGame, Singleton
   
      game: TGame = Singleton.get('Game')
      game.run()

If your game uses collisions, configuration of collision layers has not yet been implemented and must be enabled before your game starts running (though it is technically still possible to enable them at runtime). Bot layers in :func:`~base_game.core.systems.CollisionSystem.enable_collision` are interchangeable and each unique enabled combination must therefore only be registered once. Collision layers may collide with themselves and will ignore gameobjects colliding with themselves.

.. code-block:: python
   :emphasize-lines: 1,2,3,4

   TGame().system_controller.collision_system.enable_collision(
       'collision_layer_1',
       'collision_layer_2'
   )
   TGame().run()
   pg_engine.quit()  # cleaning up like responsible developers

.. note::
   
   hot reloading is not supported, though everything from standard pygame still applies.