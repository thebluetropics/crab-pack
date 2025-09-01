from . import (
	network_handler
)

def apply_client():
	network_handler.apply('client')

def apply_server():
	network_handler.apply('server')

__all__ = [apply_client.__name__, apply_server.__name__]
