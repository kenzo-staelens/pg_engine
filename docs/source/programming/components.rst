.. _programming_components:

Components
==========

Components are something you may want to create for specialized data or systems you want to use not provided by this module. In this section i will attempt to explain creating, registering and using custom components. A first important point to note is that all components should inherit from :class:`~pg_engine.core.bases.lib_abstract.TComponent` as it is assumed all components have a ``source`` attribute used for ownership and an ``update`` method which gets called every frame. For this tutorial we will be making a dummy component without much functionality.

.. warning::

   a lot of builtin components have additional base classes requiring more properties and methods to be defined like :class:`~pg_engine.components.transform_component.TransformComponent` having :class:`~pg_engine.core.bases.lib_abstract.TTransformComponent` as a base class. While other components like :class:`~pg_engine.components.sprite_component.SpriteComponent` inherit from both :class:`~pg_engine.core.bases.lib_abstract.TComponent` and :class:`~pg_engine.core.bases.lib_abstract.TRenderable` such that it can be used in the renderer system.

.. code-block:: python
   :emphasize-lines: 1,3,7,8

   from pg_engine.core import TComponent
      
   class MyComponent(TComponent):
       def __init__(self, **kw):
            super().__init__(**kw)  

       def update(self, dt: int) -> None:
           print(f'update on {self.source} called after {dt} milliseconds.')

With the above code a valid component now exists (it's ``source`` parameter being handled by the superclass) though it cannot be added to a gameobject yet as PG_Engine does not know it exists within the environment. For that we use the :func:`pg_engine.core.initializer.Initializer.add_hooks` method.

.. code-block:: python
   :emphasize-lines: 2,3,12,13,14,15

   from pg_engine.core import TComponent
   from pg_engine.core.registry import ClassRegistry
   from pg_engine.core.initializer import Initializer
      
   class MyComponent(TComponent):
       def __init__(self, **kw):
            super().__init__(**kw)  

       def update(self, dt: int) -> None:
           print(f'update on {self.source} called after {dt} milliseconds.')

   Initializer.add_hooks(
        lambda to_register=MyComponent: ClassRegistry.register(to_register),
        None,  # we don't need an unregister hook here
    )

At this point it is possible to use this component (as 'MyComponent') like in :ref:`config_gameobjects`, add custom methods and properties you might want to call or add extra parameters to ``__init__`` to customize the component further.

.. hint::

    when defining multiple components it may be easier to register them all at once in an ``__init__.py`` file.
