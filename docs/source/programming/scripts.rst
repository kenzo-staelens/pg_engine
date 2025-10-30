.. _programming_scripts:

Scripts
=======

Using components provided it is possible to perform a number of standard actions within your game, though just rendering a sprite without any logic does not make a very compelling game. For such business logic scripts are an ideal way to modify the behaviour of your game objects without having to modify engine code itself (or worse, reimplement it). They are intended to be registered once and reusable across multiple entities.

In :ref:`config_scripts` a script was already provided, in this section we will be taking a deeper look at how scripts can be written.

All scripts inherit from the class :class:`~pg_engine.api.interface_script.IScript` and must have a value for :term:`__exports__` to be usable on a gameobject (``__exports__`` may be empty for scripts that are used in inheritance)

.. code-block:: python
    :emphasize-lines: 3,4

    from pg_engine.api import IScript

    class MoveScript(IScript):
        __exports__ = 'move_script'

Even though the above scripts is valid in terms of minimum requirements it still is not able to do much. To make the script a little more useful let's start off by defining some parameters it can be configured with and add some code to it's :func:`~pg_engine.api.interface_script.IScript.update` method.

For example have the gameobject move down by a couple of pixels per millisecond. Under normal circumstances ``update`` gets called once per frame, being passed the time passed since the last frame through the parameter ``dt`` in milliseconds.


.. code-block:: python
   :emphasize-lines: 6,8,10,11

   from pg_engine.api import IScript

   class MoveScript(IScript):
       __exports__ = 'move_script'

       def __init__(self, step: float, **kw):
           super().__init__(**kw)
           self.step = step

       def update(self, dt: int) -> None:
           self.source.transform.move((self.step / dt, 0))

.. note::

   Although a script's direct parent is a variant of :class:`~pg_engine.components.script_component.ScriptComponent` (see :ref:`config_gameobjects` for an example), a script's source property points to the gameobject it belongs to. The component is used as an anchor for the script to be loaded into.

   When accessing a script by name access using ``<YourScriptComponent>.script`` is still required.

.. hint::

   When composing multiple scripts or using different system/gameinstance classes parameters may differ from game to game or library version. using ``**kw`` in init and only extracting the parameters your script is interested in will make it easier to manage this kind of dynamic behaviour. PG_Engine liberaly makes use of this kind of parameter abstraction.

Handling everything in an update loop still causes a few issues though, for one, performance overhead checking for game states and then not doing anything. Another issue is that we still cannot respond to events sent to this object, it's scene or one that's being broadcasted.

In our example for a player movement script we would like to respond to a user's keyboard input, pygame provides an event for that :py:attr:`pygame.KEYDOWN`. This can be done through the event system and it's provided :class:`~pg_engine.systems.event_system.EventListener`, :class:`~pg_engine.systems.event_system.Scope` and :func:`~pg_engine.systems.event_system.listen`

Here EventListener handles registering methods of a script marked as eventlisteners into the eventsystem though is itself *not* a subclass of IScript. ``listen`` is the decorator method responsible for marking a method as an eventlistener, it takes parameters ``event_type``, this is an integer, the event type/id created by pygame, and a scope to which the listener applies.

.. code-block:: python
   :emphasize-lines: 3,5, 12,13,14

   import pygame
   from pg_engine.api import IScript
   from pg_engine.systems import EventListener, Scope, listen

   class MoveScript(IScript, EventListener):
       __exports__ = 'move_script'

       def __init__(self, step: int, **kw):
           super().__init__(**kw)
           self.step = step

       @listen(event_type=pygame.KEYDOWN, scope=Scope.BROADCAST)
       def listen_movement(self, event: pygame.event.Event) -> None:
           self.source.transform.move((self.step / dt, 0))

There are 3 scopes a listener can use,
- LOCAL: Only handles events explicitly sent to this entity.

- BROADCAST_SCENE: Only handles events if the event is sent to a scene this entity resides in.

- BROADCAST: Only handles events broadcasted everywhere (even inactive scenes).

.. warning::
   events originating from other sources than our own code will always be using BROADCAST as this is the default.

here we define a method ``listen_movement``, it's only parameter is always going to be the event it is handling by virtue of being decorated as an eventhandler. It will be listening to ``pygame.KEYDOWN`` broadcasted events and move down the same way it did in the update loop but this time only when we press any key on our keyboard.

For completeness we should only handle the keys we are interested in (here arrow keys) and otherwise let the event pass, implementations of your business logic will depend on the event's data, type and your intentions.

.. code-block:: python
   :emphasize-lines: 18,19,21,23,25

   import pygame
   from pg_engine.api import IScript
   from pg_engine.systems import (
       EventListener,
       Scope,
       listen,
   )

   class MoveScript(IScript, EventListener):
       __exports__ = 'move_script'

       def __init__(self, step: int, **kw):
           super().__init__(**kw)
           self.step = step

       @listen(event_type=pygame.KEYDOWN, scope=Scope.BROADCAST)
       def listen_movement(self, event: pygame.event.Event) -> None:
           match event.key:
               case pygame.K_LEFT:
                   self.source.transform.move((-self.step, 0))
               case pygame.K_RIGHT:
                   self.source.transform.move((self.step, 0))
               case pygame.K_UP:
                   self.source.transform.move((0, -self.step))
               case pygame.K_DOWN:
                   self.source.transform.move((0, self.step))

.. attention::

   there is currently a bug where attempting to override an existing event listener will use *only* the original implementation of the handler.
