from . import player_inventory

def apply_client():
	player_inventory.apply_client()

def apply_server():
	pass

__all__ = [apply_client.__name__, apply_server.__name__]
