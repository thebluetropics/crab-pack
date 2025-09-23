from . import world

def apply_client():
	world.apply('client')

def apply_server():
	world.apply('server')

__all__ = [apply_client.__name__, apply_server.__name__]
