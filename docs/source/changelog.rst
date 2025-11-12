.. _changelog:

Changelog
=========

**version 1.1.0**
-----------------

New Components
..............

- **AudioSystem** - A system for handling audio files
- **ExtendedSystemController** - A systemcontroller that can include additional arbitrary systems
- **ISerializable** - A Serialization interface for saving and loading a gamestate

Other Features
..............

- The ``include`` yaml constructor can now be used recursively
- Sprites can be configured to have a set size, regardless of the incoming asset


Internal Changes
................

- Moved interface classes to a dedicated submodule "api"
- Moved Singleton (class), PostInit (metaclass) and registries to "api"
- Renamed interfaces to match industry naming standards
- Moved UI Engine Components to dedicated submodule "gui_extensions"
- Fixes to typing to allow running with pygame

**version 1.0.0**
-----------------

Initial release
