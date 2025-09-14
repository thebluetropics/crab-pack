from . import (farmland_block, block, solid_grass_block, plant_block, mortar)
import mod

def apply_client():
	if mod.config.is_feature_enabled('etc.no_crop_trampling') or mod.config.is_feature_enabled('etc.extended_farmland_water_source'):
		farmland_block.apply('client')
	block.apply('client')
	solid_grass_block.apply('client')
	plant_block.apply('client')
	mortar.apply('client')

def apply_server():
	if mod.config.is_feature_enabled('etc.no_crop_trampling') or mod.config.is_feature_enabled('etc.extended_farmland_water_source'):
		farmland_block.apply('server')
	block.apply('server')
	solid_grass_block.apply('server')
	plant_block.apply('server')
	mortar.apply('server')

__all__ = [apply_client.__name__, apply_server.__name__]
