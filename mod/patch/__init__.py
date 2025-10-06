from . import (block, entity, client, item, server, world, meta_inf, packet, recipe, network, screen)
from . import blackbox, inventory, zoom, actions

def apply_client_patches():
	block.apply_client()
	item.apply_client()
	world.apply_client()
	entity.apply_client()
	client.apply()
	packet.apply_client()
	recipe.apply_client()
	network.apply_client()
	screen.apply_client()

	meta_inf.apply_client()
	blackbox.apply('client')
	zoom.apply('client')
	inventory.apply_client()
	actions.apply('client')

def apply_server_patches():
	block.apply_server()
	server.apply()
	world.apply_server()
	packet.apply_server()
	item.apply_server()
	recipe.apply_server()
	entity.apply_server()
	network.apply_server()
	screen.apply_server()
	blackbox.apply('server')
	inventory.apply_server()
	zoom.apply('server')

	meta_inf.apply_server()

__all__ = [apply_client_patches.__name__, apply_server_patches.__name__]
