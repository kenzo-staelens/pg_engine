.. _config_root:

Root Config
===========

The root configuration file itself does not contain your game's configuration. What it does contain the information on how to load your game's configuration, which it does so in 6 stages.

- Game
- Display
- Sprites
- Scripts
- Game Objects
- UI

Where as a minimum requirement `Sprites` should be loaded after `Display` due to a dependency on display mode set in the Display configuration. Additionally Game Object should be loaded after `Sprites` and `Scripts` due to equivalent dependencies.

A single of the abovementioned 6 entries follows the following structure (for more information check out :term:`Loaders` and :term:`Processors`)

.. code-block:: yaml

   loader: <loader class>
   config: <file containing this key's configuration>
   registry: <optional, registry to load into>
   loader_args: <optional, mapping of arguments for the loader>
   processor: <optional, processor class>
   processor_args: <optional, mapping of arguments for the processor>

Even though filling in a registry is not required, it is *highly* encouraged to do so as most built in loaders will write to the provided registry.

PG_Engine provides predefined loaders and processors to quickly start up with but feel free to write your own if the ones provided are not able to load data for your specific game. If you are just following along without getting into too much custom implementation i have written a configuration which can get you started.

.. code-block:: yaml

   game:
     loader: YamlLoader
     config: config/game.yml
     processor: GameConfigProcessor
   display:
     loader: YamlLoader
     config: config/display.yml
     processor: GraphicsProcessor
     loader_args:
       useref: config/ref.yml
   sprites:
     loader: SpriteLoader
     config: config/sprites.yml
     registry: AssetRegistry
   scripts:
     loader: ScriptLoader
     config: scripts
     registry: ScriptRegistry
   objects:
     loader: GameObjectLoader
     config: config/gameobjects.yml
     registry: ObjectRegistry
     loader_args:
       useref: config/ref.yml
   ui:
     loader: PygameGuiUILoader
     config: config/ui.yml
     registry: PygameGuiRegistry

and file structure

.. code-block:: text

   .
   ├── config
   │   ├── config.yml
   │   ├── display.yml
   │   ├── game.yml
   │   ├── gameobjects.yml
   │   ├── ref.yml
   │   ├── sprites.yml
   │   └── ui.yml
   ├── gameobjects
   │   └── *.yml
   └── scripts
       ├── __init__.py
       └── *.py


Further sections in this quickstart will be using the above configuration.

