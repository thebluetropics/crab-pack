from . import world

def apply_client():
	world.apply_client()

def apply_server():
	world.apply_server()

__all__ = [apply_client.__name__, apply_server.__name__]
