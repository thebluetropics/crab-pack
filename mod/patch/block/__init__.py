from . import (block, solid_grass_block, plant_block, mortar, smelter_block, smelter_block_entity, block_entity)
from . import (persistent_leaves_block, leaves_block)
import mod

def apply_client():
	block.apply('client')
	solid_grass_block.apply('client')
	plant_block.apply('client')
	mortar.apply('client')
	block_entity.apply('client', 0)

	if mod.config.is_feature_enabled('block.smelter'):
		smelter_block.apply('client')
		smelter_block_entity.apply('client')

	if mod.config.is_feature_enabled('block.persistent_leaves'):
		persistent_leaves_block.apply('client')

	leaves_block.apply('client')

def apply_server():
	block.apply('server')
	solid_grass_block.apply('server')
	plant_block.apply('server')
	mortar.apply('server')
	block_entity.apply('server', 1)

	if mod.config.is_feature_enabled('block.smelter'):
		smelter_block.apply('server')
		smelter_block_entity.apply('server')

	if mod.config.is_feature_enabled('block.persistent_leaves'):
		persistent_leaves_block.apply('server')

	leaves_block.apply('server')

__all__ = [apply_client.__name__, apply_server.__name__]
