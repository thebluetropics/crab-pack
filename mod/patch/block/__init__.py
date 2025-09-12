from . import (farmland_block, block, solid_grass_block)

def apply_client():
	farmland_block.apply('client')
	block.apply('client')
	solid_grass_block.apply('client')

def apply_server():
	farmland_block.apply('server')
	block.apply('server')
	solid_grass_block.apply('server')

__all__ = [apply_client.__name__, apply_server.__name__]
