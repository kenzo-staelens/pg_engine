import importlib
import logging
from pathlib import Path
from types import ModuleType

from pg_engine.api import ILoader, IScript

logger = logging.getLogger(__name__)


class ScriptLoader(ILoader):

    """Specialized loader for loading external (non engine) script files."""

    def load(self) -> dict[str, IScript]:
        """
        Load scripts from a directory and it's subdirectories into :class:`ScriptRegistry`.

        filename in this class is used as the root directory of scripts instead.

        :return: A mapping of a script's :term:`__exports__` key to the script object.
        :rtype: dict[str, IScript]
        """  # noqa: E501
        loaded: dict[str, IScript] = {}
        p = Path(self.root / self.filename)
        for file in p.iterdir():
            if file.stem.startswith('__') and file.stem != '__init__':
                continue
            scriptfile: Path = p / file.stem
            module_path = str(
                scriptfile.as_posix(),
            ).replace(
                # trimming because we get some wack paths otherwise
                str(self.root.as_posix()) + '/',
                '',
            ).replace('/', '.')
            module = importlib.import_module(module_path)
            exported = self.export_module(module)
            for export_key, export in exported:
                if export_key in loaded:
                    logger.error(
                        'while loading script %s[%s] another '
                        'entry [%s] was already found. Consider using __all__.',
                        export_key,
                        export.__name__,
                        loaded[export_key].__name__,
                    )
                    continue
                logger.debug('Registered script %s', export_key)
                self.register_loaded(export_key, export)
                loaded[export_key] = export
        return loaded

    @classmethod
    def export_module(cls, module: ModuleType) -> list[tuple[str, IScript]]:
        """
        Load all exportable :class:`IScript` classes from file or module.

        .. hint::
            if a module has `__all__` defined only exportable scripts listed will\
            be processed, this is useful when extending scripts where the import would\
            otherwise be attempted to exported again.

        :param module: imported module to load scripts from.
        :type module: ModuleType
        :return: list of a script's :term:`__exports__` and class definition
        :rtype: list[tuple[str, IScript]]
        """
        # for easier sanity checking after returning
        # from this module we use a list
        # instead of joining loaded | exported
        exports: list[tuple[str, IScript]] = []
        module_all = module.__all__ if hasattr(module, '__all__') else dir(module)
        for entry in module_all:
            module_entry = getattr(module, entry)
            if (
                not isinstance(module_entry, type)
                or not issubclass(module_entry, IScript)
            ):
                continue
            if hasattr(module_entry, '__exports__') and bool(module_entry.__exports__):
                exports.append(
                    (module_entry.__exports__, module_entry),
                )
        return exports
