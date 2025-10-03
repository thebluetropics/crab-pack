from . import (player_entity, squid_entity, server_player_entity)

def apply_client():
	player_entity.apply('client')
	squid_entity.apply('client')

def apply_server():
	player_entity.apply('server')
	squid_entity.apply('server')
	server_player_entity.apply()

__all__ = [apply_client.__name__]
