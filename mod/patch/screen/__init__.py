from . import smelter_screen_handler, smelter_output_slot
import mod

def apply_client():
	if mod.config.is_feature_enabled('block.smelter'):
		smelter_screen_handler.apply('client')
		smelter_output_slot.apply('client')

def apply_server():
	if mod.config.is_feature_enabled('block.smelter'):
		smelter_screen_handler.apply('server')
		smelter_output_slot.apply('server')

__all__ = [apply_client.__name__]
