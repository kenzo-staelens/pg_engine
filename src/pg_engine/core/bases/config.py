from __future__ import annotations

from typing import Any, Required, TypedDict

import pygame

from pg_engine.api import IGameObject, IScript, Singleton

"""
Collection of all configurations possible in yaml format.

.. note::
    configuration keys are not limited to the below listed. but the below listed
    are required/supported by default.
"""


class TInstanceConfig(TypedDict, total=False):
    #: list of already loaded singletons or their registered classes
    singleton_instances: list[Singleton] | list[str]

    #: scenes in this gameinstance (automatically includes "default")
    scenes: Required[list[str]]

    #: whether debug mode should be enabled
    debug_mode: bool

    #: maximum fps of the game
    fps: int


class TLoadableConfig(TypedDict, total=False):
    #: loader class used to load a part of configuration
    loader: Required[str]
    #: custom parameters passed to the loader class
    loader_args: dict[str, Any]
    #: configuration file to load from
    config: Required[str]
    #: process class used to post process the loaded data
    processor: str
    #: custom parameters passed to the processor
    processor_args: dict[str, Any]
    #: registry to store loaded data into
    registry: str


class TConfigFile(TypedDict, total=True):

    """Required keys in the root config file."""

    game: TLoadableConfig
    display: TLoadableConfig
    sprites: TLoadableConfig
    scripts: TLoadableConfig
    objects: TLoadableConfig
    ui: TLoadableConfig


class DisplayModeKey(TypedDict, total=True):
    #: size of the display window
    size: tuple[int, int]


class TRendererConfig(TypedDict, total=True):
    # pygame display mode data
    display_mode: DisplayModeKey


class TUIManagerConfig(TypedDict, total=True):
    #: window resolution of the UI
    window_resolution: tuple[int, int]


class TDisplayConfig(TypedDict, total=True):
    renderer: TRendererConfig
    uimanager: TUIManagerConfig


class LoadedGameConfig(TypedDict):
    singleton_instances: list[Singleton]
    debug_mode: bool
    fps: int


class TGlobalGameConfig(TypedDict):

    """Fully loaded data for a gameinstance."""

    game: LoadedGameConfig
    display: TDisplayConfig
    sprites: dict[str, pygame.Surface]
    scripts: dict[str, IScript]
    objects: dict[str, IGameObject]
    ui: dict[str, Any]


class TSpriteConfig(TypedDict):
    #: file to load sprites from
    filename: str
    #: number of sprites width-wise
    width: int
    #: number of sprites height-wise
    height: int
    #: size and starting point the first sprite
    rect: tuple[int, int, int, int]
    #: colorkey of the spritesheet
    colorkey: tuple[int, int, int]
    #: names of sprites left to right, then top to bottom
    bindings: list[str]


class TComponentConfig(TypedDict, total=False):
    #: class of the component as registered in ClassRegistry
    type: Required[str]
    #: optional component name to prevent access by name collisions
    refname: str | None
    #: arguments passed to the component class
    args: Required[dict[str] | None]


class TGameObjectConfig(TypedDict, total=False):
    #: scene the component is constructed
    scene: Required[str | None]
    #: list of components the gameobject consists of
    components: Required[list[TComponentConfig]]
    # whether the gameobject is a spawnable template
    prefab: bool


class TUIConfig(TypedDict, total=False):
    classpath: Required[str]
    size: Required[tuple[int, int]]
    offset: Required[tuple[int, int]]
    anchors: dict[str, str] | None
    args: dict[str, Any]


__all__ = [
    'TComponentConfig',
    'TConfigFile',
    'TDisplayConfig',
    'TGameObjectConfig',
    'TGlobalGameConfig',
    'TInstanceConfig',
    'TLoadableConfig',
    'TRendererConfig',
    'TSpriteConfig',
    'TUIConfig',
    'TUIManagerConfig',
]
