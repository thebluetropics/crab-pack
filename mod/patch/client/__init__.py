from . import (
	title_screen,
	minecraft,
	hud,
	assets,
	keyboard_input,
	game_renderer,
	i18n,
	client_network_handler,
	item_renderer,
	world_renderer,
	entity_renderer,
	block_render_manager,
	client_player_entity,
	smelter_screen,
	singleplayer_interaction_manager,
	handled_screen
)
import mod

def apply():
	title_screen.apply()
	minecraft.apply()
	hud.apply()
	assets.apply()
	keyboard_input.apply()
	game_renderer.apply()
	i18n.apply()

	client_network_handler.apply()

	item_renderer.apply()
	world_renderer.apply()
	entity_renderer.apply()
	block_render_manager.apply()

	if mod.config.is_feature_enabled('block.smelter'):
		smelter_screen.apply()
		client_player_entity.apply()

	singleplayer_interaction_manager.apply()
	handled_screen.apply()

__all__ = [title_screen.__name__]
