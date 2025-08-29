from . import (farmland_block, block)

def apply_client():
	farmland_block.apply('client')
	block.apply_client()

def apply_server():
	farmland_block.apply('server')
	block.apply_server()

__all__ = [apply_client.__name__, apply_server.__name__]
