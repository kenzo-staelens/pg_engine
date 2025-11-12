
from pg_engine.core.bases.initializer import Initializer
from pg_engine.api.registry import ClassRegistry

from .something import SomeClass

for to_register in [
    SomeClass,
]:
    Initializer.add_hooks(
        lambda to_register=to_register: ClassRegistry.register(to_register),
        None,
    )
