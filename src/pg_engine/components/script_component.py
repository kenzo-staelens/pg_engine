from __future__ import annotations

from typing import Any

from pg_engine.api import IComponent, IScript
from pg_engine.api.registry import ScriptRegistry


class ScriptComponent(IComponent):
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
        script_class: type[IScript] = ScriptRegistry.get(scriptname)
        self.script: IScript = script_class(**args, source=self)

    def update(self, dt: int) -> None:
        """
        Pass the update call on to this component's script.

        :param dt: number of milliseconds since the last frame
        :type dt: int
        """
        self.script.update(dt)
