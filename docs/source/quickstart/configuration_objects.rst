.. _config_gameobjects:

GameObject Configuration
========================

The configuration for game objects is possibly one of the most important configurations you'll be using. To keep gameobjects organised i would recommend writing configurations for single game objects into separate files and using the :term:`include` constructor to load all of them in a single loadable config. After this section you should be able to move a little red square around the screen.

.. hint::

    included files can make use of the same reference file used for the loading of the file they are included in.

.. code-block:: yaml
   :emphasize-lines: 6

   objects:
     loader: GameObjectLoader
     config: config/gameobjects.yml
     registry: ObjectRegistry
     loader_args:
       useref: config/ref.yml

.. collapse:: content of gameobjects.yml

   .. code-block:: yaml

      simple_gameobject: !include gameobjects/simple_gameobject.yml

For the sake of this tutorial we will be constructing a simple gameobject using data already loaded before in :ref:`config_scripts` and :ref:`config_sprites`

.. code-block:: yaml

   scene: default
   prefab: false
   components:
     - type: TransformComponent2D
       args:
         x: 0
         y: 0
     - type: SpriteComponent
       args:
         asset: red
         layer: 1
     - type: ScriptComponent
       refname: move_script
       args:
         scriptname: move_script
         args:
           step: 32

Despite this configution being fairly short, a lot of things are still happening. First off is the ``scene`` key, it tells the program where a game object will be spawned into. The key (nor value) is required and will default to the "default" scene. Objects in different scenes will not be able to interract with eachother.

A second value in the above configuration is ``prefab``, although it is not defined in any configuration file, when using the :class:`~pg_engine.core.loaders.game_object_loader.GameObjectLoader` instead of trying to load a gameobject into the game world it's definition will be stored in the :term:`PrefabRegistry` for easier access to scripts (see also :func:`pg_engine.api.interface_game.IGame.spawn`).

the last part of defining a game object is it's components. PG_Engine is based on an Entity Component System (`ECS <https://en.wikipedia.org/wiki/Entity_component_system>`_ for short), therefore each component is responsible for one task on the gameobject, like tracking it's position, holding on to rendering data, etc. ``components`` is a list of mappings with two required keys (each) to be considered valid.

.. code-block:: yaml
   :emphasize-lines: 2,3,4,5

   components:
     - type: TransformComponent2D
       args:
         x: 20
         y: 20
     - type: SpriteComponent
       args:
         asset: red
         layer: 1
     - type: ScriptComponent
       refname: move_script
       args:
         scriptname: move_script
         args:
           step: 32

The first requirement is a type, like :class:`~pg_engine.components.transform_component.TransformComponent2D`, it is a class found in the :term:`ClassRegistry` (more on creating custom components in :ref:`programming_components`). The second requirement is the arguments (``args``) passed to the class's constructor, they serve as initial values for the component as soon as the game starts. Arguments may be left empty (but not omitted) if the class contains no arguments or they have defaults built into the class (like ``angle`` in this case).

.. note::

   Using the concrete implementation of :class:`~pg_engine.components.game_object.GameObject` a transform component may be omitted and one will be constructed on the fly as soon as it is requested. from the one defined in :ref:`config_gameinstance`.

   .. code-block:: yaml
      :emphasize-lines: 5,6

      !classinit
        type: GameObjectBuilder
        args:
          builder_class: !classget GameObject
          builder_kw:
            transform_class: !classget TransformComponent2D

Components can contain a third optional key ``refname``. By default a component gets registered into a gameobject by it's classname, however it is not rare for a gameobject to contain multiple scripts (eg. one to handle movement, one to handle health, ...) which would then cause name collisions when trying to register multiple components of the same type. For situations like those refname can be used to grant the component a custom name to access the component as instead of it's classname.

.. code-block:: yaml
   :linenos:
   :emphasize-lines: 10, 11

   components:
     - type: TransformComponent2D
       args:
         x: 20
         y: 20
     - type: SpriteComponent
       args:
         asset: red
         layer: 1
     - type: ScriptComponent
       refname: move_script
       args:
         scriptname: move_script
         args:
           step: 32

.. note::

   Script components do take a slightly more complex argument structure as each script itself can additionally define one or more arguments to be set as default values. The outer args (line 12) take the name of an exported/imported script from :ref:`config_scripts` and keyword arguments (inner args, line 14) passed to the script's ``__init__``.

   This component's ``refname`` and ``scriptname`` can have different values.
