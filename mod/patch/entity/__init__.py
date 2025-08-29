from . import (player_entity, squid_entity, server_player_entity)

def apply_client():
	player_entity.apply_client()
	squid_entity.apply_client()

def apply_server():
	squid_entity.apply_server()
	server_player_entity.apply()
	player_entity.apply_server()

__all__ = [apply_client.__name__]
