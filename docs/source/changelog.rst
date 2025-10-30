.. _changelog:

Changelog
=========

**version 1.1.0**
-----------------

New Components
..............

- **AudioSystem** - A system for handling audio files
- **ExtendedSystemController** - A systemcontroller that can include additional arbitrary systems

Minor Features
..............

- The ``include`` yaml constructor can now be used recursively


Internal Changes
................

- Moved interface classes to a dedicated submodule "api"
- Moved Singleton (class), PostInit (metaclass) and registries to "api"
- Renamed interfaces to match industry naming standards
- Moved UI Engine Components to dedicated submodule "gui_extensions"

**version 1.0.0**
-----------------

Initial realease
