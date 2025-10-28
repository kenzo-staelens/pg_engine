Loading Configurations
======================

.. glossary::

   Loaders
     Loaders are responsible for converting raw data files like yaml, xml, image files, etc into a usable format for the game engine. They are designed to have as little knowledge as possible of the inner workings of the engine and do not handle engine configuration. They however can still convert data or use the available public api of the engine to handle more complex data conversions.

   Processors
     Unlike loaders, processors do heavily depend on the specific implementation of engine components (though preferably cover as many variants as possible when configuring a :ref:`terms_singletons`). They accept data loaded by Loaders and perform necessary configurations on engine components or otherwise provide further post processing onto loaded data for which loaders are too broadly defined.

   Registries
     Registries are containers specialized for storing one class of objects (or subclasses thereof). PG_Engine provides several registries out of the box. For further information see :ref:`terms_registries`