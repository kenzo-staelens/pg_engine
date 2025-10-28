import pathlib

import pg_engine
from pg_engine.core import GameConfigLoader, TGame

pg_engine.init()

config_root = pathlib.Path(__file__).parent

GameConfigLoader(
    filename='config/config.yml',
    root=config_root,
).load()

TGame().run()
pg_engine.quit()
