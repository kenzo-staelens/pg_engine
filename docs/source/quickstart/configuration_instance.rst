.. _config_gameinstance:

Game Instance Configuration
===========================

First of the configuration keys, ``game`` defined as (at minimum) :class:`~pg_engine.core.bases.config.TInstanceConfig`

this configuration, it's loaders and it's processors are responsible for instantiating all singleton instances used by the engine and configuring the main game instance (:term:`__singleton_key__` :term:`Game`)

using the configuration provided in :ref:`config_root`

.. code-block:: yaml

   game:
     loader: YamlLoader
     config: config/game.yml
     processor: GameConfigProcessor

and a referenced configuration file

.. code-block:: yaml

   scenes:
     - default
     - main_scene
   debug_mode: false
   fps: 60
   singleton_instances:
     - !classinit CollisionSystem
     - !classinit EventSystem
     - !classinit BaseSystemController

     - !classinit Camera2D
     - !classinit BaseRenderer
     - !classinit PygameGuiUIManager

     - !classinit
         type: GameObjectBuilder
         args:
           builder_class: !classget GameObject
           builder_kw:
             transform_class: !classget TransformComponent2D

     - !classinit
         type: SceneBuilder
         args:
           builder_class: !classget Scene

     - !classinit BaseGame

This example configuration contains 2 scenes, a minimum of 1 is required (being 'default')

- default, the scene the game loads on start (e.g. our title screen)
- main scene, a scene we can transition to for our game content outside of the title screen

.. note::
   the 'default' default will automatically be added by :class:`~pg_engine.core.processors.GameConfigProcessor` if it is not defined but it is here for completeness.

For more information on scene transitions see :ref:`programming_scripts`.

We also set the maximum framerate to 60 fps and disabled ``debug_mode``. Debug mode is a setting other systems can hook into but does nothing on it's own. Currently PG_Engine only uses this setting to render collider components (see :ref:`config_gameobjects` and `programming_gameobjects`)

A last piece of the puzzle is the ``singleton_instances`` key, in this example we are using the :term:`classinit` and :term:`classget` yaml constructors defined by PG_Engine to configure which classes get used by the engine. this section is a fairly powerful part of your configuration as it can modify the inner workings of PG_Engine itself if you provide a custom engine component.

.. warning::
    Singleton classes *must* use !classinit or be instantiated by the loader or processor as most engine code depends on an instance existing.

.. warning::
   Note the order in which classes get initialized in this configuration, such as ``BaseSystemController`` being initialized *after* the systems or ``BaseBame`` last. This is due to internal dependencies due to these classes requiring instances of other Singletons existing.
