from __future__ import annotations

from typing import Any

from pg_engine.core import TComponent, TScript
from pg_engine.core.bases.registry import ScriptRegistry


class ScriptComponent(TComponent):
    def __init__(
        self,
        scriptname: str,
        args: dict[str, Any] | None = None,
        **kw,
    ):
        """
        Initialize the script and it's underlying script component.

        :param scriptname: the script to link referencing it's :term:`__exports__` key
        :type scriptname: str
        :param values: keyword args passed onto the script object, defaults to None
        :type values: dict[str, Any] | None, optional
        """
        super().__init__(**kw)
        if args is None:
            args = {}
        script_class: type[TScript] = ScriptRegistry.get(scriptname)
        self.script: TScript = script_class(**args, source=self)

    def update(self, dt: int) -> None:
        """
        Pass the update call on to this component's script.

        :param dt: number of milliseconds since the last frame
        :type dt: int
        """
        self.script.update(dt)
