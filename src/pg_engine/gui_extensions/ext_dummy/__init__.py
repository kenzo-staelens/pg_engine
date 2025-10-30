from pg_engine.core import ClassRegistry, Initializer
from .dummy_loader import DummyUILoader
from .dummy_manager import DummyUIManager


for to_register in [
    DummyUIManager,
    DummyUILoader,
]:
    Initializer.add_hooks(
        lambda c=to_register: ClassRegistry.register(c),
        None,
    )

__all__ = [
    'DummyUILoader',
    'DummyUIManager',
]
