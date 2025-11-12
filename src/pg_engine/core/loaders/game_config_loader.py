from __future__ import annotations

import logging
import pathlib
import sys
from typing import Any, cast

from pg_engine.api import (
    IGame,
    ILoader,
    IProcessor,
    IRegistry,
)
from pg_engine.api.registry import ClassRegistry
from pg_engine.core import (
    Context,
    Initializer,
    TConfigFile,
    TGlobalGameConfig,
    TLoadableConfig,
)
from pg_engine.core.exit_codes import ExitCodes

from .yaml_loader import YamlLoader

logger = logging.getLogger(__name__)


class GameConfigLoader(YamlLoader):

    """Specialized loader for orchestrating loading of the root configuration."""

    def __init__(
        self,
        filename: str,
        root: pathlib.PosixPath,
        registry: IRegistry | None = None,
        **kw,
    ):
        super().__init__(filename=filename, root=root, registry=registry, **kw)

    @classmethod
    def _validate_configs(cls, config: TConfigFile) -> bool:
        """
        Check if a loaded root config contains all required keys.

        :param config: Loaded root config file
        :type config: TConfigFile
        :return: Whether all required keys are present
        :rtype: bool
        """
        requires = [
            'game',
            'display',
            'sprites',
            'scripts',
            'objects',
            'ui',
        ]
        valid = True
        for key in requires:
            if key in config:
                continue
            valid = False
            logger.critical(
                "Config: missing configuration '%s'",
                key,
            )
        return valid

    @classmethod
    def _validate_keys(cls, key: str, conf: TLoadableConfig) -> bool:
        """
        Check if each individual config key has it's required keys.

        :param key: Key being checked, used for logging
        :type key: str
        :param conf: Content of the configuration key
        :type conf: TLoadableConfig
        :return: Whether all required keys are present
        :rtype: bool
        """
        requires = ('loader', 'config')
        valid_config = True
        for req in requires:
            if req not in conf:
                logger.critical(
                    "Config: %s missing key '%s'",
                    key,
                    req,
                )
                valid_config = False
        return valid_config

    @classmethod
    def _validate_config_objects(
            cls,
            conf: TLoadableConfig,
            verification_objects: dict[str, Any],
        ) -> bool:
        """
        Check if all configuration loaders and processors successfully loaded.

        :param conf: content of a root configuration key
        :type conf: TLoadableConfig
        :param verification_objects: equivalent loader and processor objects.
        :type verification_objects: dict[str]
        :return: Whether loading the config was successful.
        :rtype: bool
        """
        valid = True
        # don't use dirty hack with locals, just ref from a dict
        for key, obj in verification_objects.items():
            if obj:
                continue
            valid = False
            message = (
                "Failed to acquire %s '%s', not in registry."
                if key != 'config' else
                "Failed to load %s '%s'"
            )
            logger.critical(
                message,
                key,
                conf.get(key, None),
            )
        return valid

    def load(self) -> TGlobalGameConfig:
        """
        Load game content and configuration from root config file.

        Exits when an in valid configuration is encountered.

        calls each loader/processor pair and returns a configkey with\
            the loaded content.

        :return: Full constructed game configuration.
        :rtype: TGlobalGameConfig
        """
        loaded: dict[str, Any] = {}
        with Context(evaluate_lazy=False):
            game_config: TConfigFile = cast('TConfigFile', super().load() or {})

            if not self._validate_configs(game_config):
                sys.exit(ExitCodes.EXIT_CODE_INVALID_CONFIG)

            for key, conf in game_config.items():
                conf = cast('TLoadableConfig', conf)
                if not self._validate_keys(key, conf):
                    sys.exit(ExitCodes.EXIT_CODE_INVALID_KEYS)

                # aqcuire loaders and processors
                loader: type[ILoader] | None = cast(
                    'type[ILoader] | None',
                    ClassRegistry.get(conf['loader']),
                )
                if loader is None:
                    logger.critical('loader %s does not exist', conf['loader'])
                    sys.exit(ExitCodes.EXIT_CODE_FATAL_CONSTRUCT)
                loader = cast('type[ILoader]', loader)
                loader_args: dict = conf.get('loader_args') or {}
                processor_args = {}
                if 'processor' in conf:
                    processor: type[IProcessor] | None = cast(
                        'type[IProcessor] | None',
                        ClassRegistry.get(conf['processor']),
                    )
                    if processor is None:
                        logger.critical('loader %s does not exist', conf['loader'])
                        sys.exit(ExitCodes.EXIT_CODE_FATAL_CONSTRUCT)
                    # also convert explicit none to {}
                    processor_args: dict[str, Any] = conf.get(
                        'processor_args',
                        {},
                    ) or {}
                else:
                    # keep it as a dummy
                    # though invalid processors still get flagged
                    processor: type[IProcessor] = cast(
                        'type[IProcessor]',
                        type(
                            'DummyProcessor',
                            (IProcessor,),
                            {'process': lambda _, __: None},
                        ),
                    )

                if not self._validate_config_objects(
                    conf,
                    {
                        'loader': loader,
                        'config': conf['config'],
                        'processor': processor,
                    },
                ):
                    sys.exit(ExitCodes.EXIT_CODE_INVALID_OBJECT)

                # doing the actual work

                loaded[key] = loader(
                    filename=conf['config'],
                    registry=conf.get('registry'),
                    root=self.root,
                    **loader_args,
                ).load()
                cast('IProcessor', processor).process(loaded[key], processor_args)
        return cast('TGlobalGameConfig', loaded)

    @classmethod
    def runfrom(cls, config: str) -> None:
        """
        Load and instantly run from root configuration file.

        :param config: configuration file path.
        :type config: str
        """
        Initializer.init()
        cls(config).load()
        IGame().run()
