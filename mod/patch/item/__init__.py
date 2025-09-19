from . import (food_item, item, bottle_item, dye_item, pickaxe_item, axe_item, seeds_item)
import mod

def apply_client():
	food_item.apply('client')
	item.apply('client')
	bottle_item.apply('client')
	pickaxe_item.apply('client')
	axe_item.apply('client')
	seeds_item.apply('client')

	if mod.config.is_feature_enabled('block.solid_grass_block') or mod.config.is_feature_enabled('etc.dirt_to_grass_block'):
		dye_item.apply('client')

def apply_server():
	food_item.apply('server')
	item.apply('server')
	bottle_item.apply('server')
	pickaxe_item.apply('server')
	axe_item.apply('server')
	seeds_item.apply('server')

	if mod.config.is_feature_enabled('block.solid_grass_block') or mod.config.is_feature_enabled('etc.dirt_to_grass_block'):
		dye_item.apply('server')

__all__ = [apply_client.__name__]
