.. _config_scripts:

Script Configuration
====================

Scripts are a second large part of game objects which cannot be defined purely in yaml, you'd likely use python for that instead. to make things easy we'll be loading scripts from a python "package" instead (i.e. an ``__init__.py`` file is required). For creating scripts see :ref:`programming_scripts`.

For this example i will be showing two ways scripts get loaded by the builtin ScriptLoader.

.. code-block:: yaml

  scripts:
     loader: ScriptLoader
     config: scripts
     registry: ScriptRegistry

.. code-block:: text

   scripts
   ├── __init__.py
   └── move_script.py

.. collapse:: Optional content of __init__.py
   
   .. code-block:: python

      from pg_engine.base_scripts import OOBCleanup


.. collapse:: Content of move_script.py

   .. code-block:: python

      import pygame

      from pg_engine.core import TScript
      from pg_engine.systems import (
          EventListener,
          Scope,
          listen,
      )
      
      class MoveScript(TScript, EventListener):
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
      
      __all__ = [
          'MoveScript',
      ]


The first option is loading scripts directly from the ``__init__.py`` file, a good example is if you want to make use of ``oob_cleanup``, a script used to clean up gameobjects that are considered out of bounds and should be destroyed.

the second method is providing script files as is in the scripts directory (``config`` key) or subpackages thereof. Up above we defined a script MoveScript which we wish to use in our game. A problem that could occur here is that we are extending off of another script. Here this is not the case with EventListener as it is technically not a script but could be the case with the import some other script which we do not want to export into our game. in situations like this ``__all__`` can be used to filter out which scripts should be made available for exports.

.. note::

   only scripts with :term:`__exports__` set will be exported

.. warning::
    
   Use ``__init__.py`` only to load scripts from external sources into your game.
   If scripts are already being provided in the scripts directory this will cause PG_Engine to attempt to load the scripts twice.