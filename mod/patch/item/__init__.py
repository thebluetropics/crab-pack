from . import (food_item, item, bottle_item, dye_item, pickaxe_item)

def apply_client():
	food_item.apply('client')
	item.apply('client')
	bottle_item.apply('client')
	dye_item.apply('client')
	pickaxe_item.apply('client')

def apply_server():
	food_item.apply('server')
	item.apply('server')
	bottle_item.apply('server')
	dye_item.apply('server')
	pickaxe_item.apply('server')

__all__ = [apply_client.__name__]
