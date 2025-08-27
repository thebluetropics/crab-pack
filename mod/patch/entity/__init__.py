from . import (player_entity, squid_entity)

def apply_client():
	player_entity.apply_client()
	squid_entity.apply_client()

def apply_server():
	squid_entity.apply_server()

__all__ = [apply_client.__name__]
