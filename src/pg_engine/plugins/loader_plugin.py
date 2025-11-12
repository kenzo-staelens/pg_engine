import json
import logging
import pathlib
import sys
from enum import IntEnum
from typing import TypedDict

from pg_engine.core.exit_codes import exit_code_generator

logger = logging.getLogger(__name__)


class ExitCodePlugin(IntEnum):
    EXIT_CODE_MISSING_PLUGIN = exit_code_generator()
    EXIT_CODE_LOAD_PLUGIN = exit_code_generator()


class Manifest(TypedDict):
    name: str
    version: str
    author: str
    license: str
    requires: list[str]


class PluginLoader:
    # https://en.wikipedia.org/wiki/Transitive_reduction
    def __init__(self, load_path: pathlib.PosixPath):
        self.load_path = load_path
        self.graph = self.load_dependency_graph()

    @staticmethod
    def load_manifest(path: pathlib.PosixPath) ->  Manifest:
        with open(path) as f:
            return json.load(f)

    def load_dependency_graph(self) -> dict[str, list[str]]:
        dependency_graph = {}
        all_dependencies = []
        for manifest in self.load_path.glob('*/manifest.json'):
            plugin = manifest.parent.stem
            manifest_content: Manifest = self.load_manifest(manifest)

            dependency_graph[plugin] = manifest_content['requires']
            all_dependencies += manifest_content['requires']
            all_dependencies.append(plugin)

        # sanity check
        dependency_delta = set(all_dependencies) - set(dependency_graph.keys())
        if dependency_delta:
            logger.critical(
                'Expected the following plugins but they are missing:\n%s',
                '\n'.join(dependency_delta),
            )
            sys.exit(ExitCodePlugin.EXIT_CODE_MISSING_PLUGIN)
        return dependency_graph

    def get_load_strategy(self) -> list[str]:
        load_stack = []
        graph = self.graph
        for key in graph:
            load_stack += self.get_single_load_strategy(key)
        # reduce this entire thing to single occurences
        # in reverse because first load dependencies then dependants
        res = []
        for item in load_stack[::-1]:
            # res list likely won't be 100000 plugins so should be fine
            # to use O(n²) algorithm here
            if item not in res:
                res.append(item)
        return load_stack

    def get_single_load_strategy(
        self,
        to_load: str,
        loop_check: set[str] | None = None,
        current: list[str] | None = None,
    ) -> list[str]:
        if current is None:
            current = []
        if loop_check and to_load in loop_check:
            loop = ', '.join([to_load, *current])
            message = f'Circular Dependency detected while loading ({loop})'
            raise RecursionError(message)
        load_stack = [to_load]
        loop_tracker = {to_load} | (loop_check or set())
        deps = self.graph.get(to_load, [])
        for item in deps:
            load_stack += self.get_single_load_strategy(
                item,
                loop_tracker.copy(),
                load_stack,
            )
        return load_stack

    def load_modules(self) -> None:
        to_load = self.get_load_strategy()
        to_load_count = len(set(to_load))
        loaded = set()
        while to_load:
            head = to_load[0]
            del to_load[0]
            if head in loaded:
                continue
            try:
                logger.info(
                    'Loading plugin %s (%s/%s)',
                    head,
                    len(loaded),
                    to_load_count,
                )
                print(f' {head}')
            except Exception:
                logger.exception(
                    'Failed to load plugin %s',
                    head,
                )
                sys.exit(ExitCodePlugin.EXIT_CODE_LOAD_PLUGIN)


if __name__ == '__main__':
    from pprint import pprint
    path = pathlib.PosixPath(
        '/home/kenzo/Desktop/pg_engine/example/quickstart_example/plugins',
    )
    loader = PluginLoader(path)
    pprint(loader.load_dependency_graph())  # noqa: T203 if name = main
    pprint(loader.get_load_strategy())  # noqa: T203
