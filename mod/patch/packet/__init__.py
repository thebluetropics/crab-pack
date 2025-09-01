from . import (
	s2c_hunger_update,
	packet
)

def apply_client():
	s2c_hunger_update.apply_client()
	packet.apply('client')

def apply_server():
	s2c_hunger_update.apply_server()
	packet.apply('server')

__all__ = [apply_client.__name__, apply_server.__name__]
