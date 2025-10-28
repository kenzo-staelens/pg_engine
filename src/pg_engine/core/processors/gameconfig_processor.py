from pg_engine.core import TGame, TProcessor
from pg_engine.core.bases.config import TInstanceConfig


class GameConfigProcessor(TProcessor):

    """Specialized processor to configure core :class:`TGame` instances."""

    @classmethod
    def process(
        cls,
        config: TInstanceConfig,
        processor_args: None = None,  # noqa: ARG003
    ) -> None:
        """
        Configure a :class:`TGame` instance after loading.

        - Construct :attr:`TInstanceConfig.scenes`
        - Add a scene 'default' if not found
        - set debug mode from :attr:`TInstanceConfig.debug_mode` (default false)
        - set maximum fps from :attr:`TInstanceConfig.fps` (default 60)

        :param config: _description_
        :type config: TInstanceConfig
        :param processor_args: not used, defaults to None
        :type processor_args: None, optional
        """
        game = TGame()

        for scene in config['scenes']:
            scene_object = game.scenebuilder.build(scene)
            game.scenes[scene] = scene_object
        if 'default' not in game.scenes:
            game.scenes['default'] = game.scenebuilder.build('default')
        game.debug_mode = config.get('debug_mode', False)
        game.fps = config.get('fps', 60)
