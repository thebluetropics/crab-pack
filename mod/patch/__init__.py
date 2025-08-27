from . import (block, entity, client, item, server, world, meta_inf, packet, recipe)

def apply_client_patches():
	block.apply_client()
	item.apply_client()
	world.apply_client()
	entity.apply_client()
	client.apply()
	packet.apply_client()
	recipe.apply_client()

	meta_inf.apply_client()

def apply_server_patches():
	block.apply_server()
	server.apply()
	world.apply_server()
	packet.apply_server()
	item.apply_server()
	recipe.apply_server()

	meta_inf.apply_server()

__all__ = [apply_client_patches.__name__, apply_server_patches.__name__]
