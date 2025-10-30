from pg_engine.core import ClassRegistry, Initializer

__all__ = []

try:
    from .pygame_gui_loader import PygameGuiUILoader
    from .pygame_gui_manager import PygameGuiUIManager
    from .pygame_gui_registry import PygameGuiRegistry
    Initializer.add_hooks(
        lambda: ClassRegistry.register(PygameGuiUILoader),
        None,
    )
    Initializer.add_hooks(
        lambda: ClassRegistry.register(PygameGuiUIManager),
        None,
    )
    Initializer.add_hooks(
        lambda: ClassRegistry.register(PygameGuiRegistry),
        PygameGuiRegistry.clear,
    )
    __all__ += [
        'PygameGuiRegistry',
        'PygameGuiUILoader',
        'PygameGuiUIManager',
    ]
except ModuleNotFoundError:
    pass
