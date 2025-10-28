# PG Engine

PG_Engine is a module to build pygame games in an ECS system much like Unity, Unreal Engine or other popular game engines through more configuration than actual code. Nearly all internals of the engine are replaceable or extensible by custom code if you would wish to do so. As is defining custom components if what is provided is lacking in functionality.

A GUI system for pygame CE.

- [Documentation](https://pg-engine.readthedocs.io/)
- [GitHub](https://github.com/kenzo-staelens/pg_engine)
- [PyPi](https://pypi.org/project/pg_engine/)

[![pypi](https://badge.fury.io/py/pg-ecs-engine.svg)](https://pypi.python.org/pypi/pg-ecs-engine)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/release/python-312/)
[![License: MIT](https://img.shields.io/badge/License-LGPL--2.1-yellow.svg)](https://opensource.org/licenses/LGPL-2-1)

## Requirements

- pyyaml
- pygame or pygame-ce (recommended)
- python>=3.12

## Installation

Due to installation conflicts when installing one of [pygame](https://www.pygame.org/) or [pygame-ce](https://pyga.me/) installing either as an optional dependency is required if neither is available on your system.

```bash
   pip install pg-ecs-engine[pygame] -U
   pip install pg-ecs-engine[pygame-ce] -U
```

Or from source

```bash
   pip install .[pygame] -U
   pip install .[pygame-ce] -U
```

Note that using the builtin UI components this library require a compatible library. PG engine provides pygame_gui for this but and requires pygame-ce if using this extension.
