from . import (
	title_screen,
	minecraft,
	hud,
	assets,
	keyboard_input,
	game_renderer,
	i18n,
	client_network_handler
)

def apply():
	title_screen.apply()
	minecraft.apply()
	hud.apply()
	assets.apply()
	keyboard_input.apply()
	game_renderer.apply()
	i18n.apply()
	client_network_handler.apply()

__all__ = [title_screen.__name__]
