UI Configuration
================

.. admonition:: Developer note

    PG_Engine currently uses a yaml schema to configure a UI. I am aware this implementation is far from ideal but an XML loader has not yet been developed for this library whereas one for yaml exists.

The last of the configurations is that of the UI. In this part of the configuration we will only be handling the layout, not the functionality (which should be done through scripts). Note that the public API of the built in UI is heavily influenced by `pygame_gui <https://pygame-gui.readthedocs.io/en/latest/index.html>`_ and thus requires use of pygame-ce over a standard pygame installation when using this library. Out of the box, this library provides a UI implementation using pygame-gui.

.. code-block:: yaml

   ui:
     loader: PygameGuiUILoader
     config: config/ui.yml
     registry: PygameGuiRegistry

.. note::
   scripts cannot be attached to UI elements, though a dummy gameobject with a :attr:`~pg_engine.systems.event_system.Scope.BROADCAST` scope can work as standin for capturing and handling UI events.

Although reading through what UI library you decide to use will be much more valuable than just trying things in this UI i would still like to point out a few things that do not involve specific implementations of one or another library though i will be using pygame_gui for this example.

.. code-block:: yaml

   start_button:
     classpath: pygame_gui.elements.UIButton
     size:
       - 100
       - 20
     offset:
       - 0
       - 0
     anchors:
       centerx: centerx
       centery: centery
     args:
       text: A button
     parent: default

To start of there are 3 required parameters, ``classpath``, ``size`` and ``offset``. Classpath here being by far the most important one, this parameter tells your program where to import a UI element from and is the same as the fully qualified import you would use in a python module (i.e. ``import pygame_gui.elements.UIButton``). Size and offset here are are used to construct the rectangle where the UI element will be placed.

.. note::
    The design decision was made to keep them split over a single ``rect`` parameter to accomodate standardized sizes from a reference file without interfering too much with tiling of multiple similar elements.

Next are anchors and args, anchors are, in this case, a specific implementation of pygame_gui and might not have any meaning if another library is being used, They are provided as a part of the public API but may certainly be omitted or left empty (more information at `pygame_gui layout_guide <https://pygame-gui.readthedocs.io/en/latest/layout_guide.html#>`_). Args as well is a parameter that may be left empty or omitted and, like most other configurations in this library defining ``args`` are used to pass extra arguments to the configured class in keyword form.

.. warning::

    when defining anchors relative to another element pygame_gui expects that element to already exist as an instance of one of it's classes.

The last parameter is ``parent``, like the above mentioned two it is also not required but is used to hierarchically structure UI elements. It simply takes the name of another UI element and will be considered a direct child inside of that element.

.. note::

   :class:`~pg_engine.gui_extensions.ext_pygame_gui.pygame_gui_loader.PygameGuiUILoader` will automatically create :py:class:`pygame_gui.core.UIContainer` instances for each scene covering the ui manager's screen space.

.. warning::

   UI elements without parent will not be managed by scene switching or UI hierarchies.


If you prefer to not use any gui elements (or otherwise have no gui library installed) PG_Engine still requires defining a UI manager and UI Loader. if none are available a :class:`~pg_engine.gui_extensions.ext_dummy.dummy_loader.DummyUILoader` and :class:`~pg_engine.gui_extensions.ext_dummy.dummy_manager.DummyUIManager` are provided to function as placeholders.

If you are following this tutorial the following changes are required to disable it's use.

.. code-block:: yaml
  :emphasize-lines: 2,3,5
  :caption: config.yml

   ui:
     # loader: PygameGuiUILoader
     loader: DummyUILoader
     config: config/ui.yml
     # registry: PygameGuiRegistry

.. code-block:: yaml
  :emphasize-lines: 12, 13
  :caption: game.yml

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
     # - !classinit PygameGuiUIManager
     - !classinit DummyUIManager
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

