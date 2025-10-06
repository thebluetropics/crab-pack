from . import (
	s2c_hunger_update,
	s2c_thirst_update,
	packet,
	actions_update_packet
)

def apply_client():
	s2c_hunger_update.apply('client')
	packet.apply('client')
	s2c_thirst_update.apply('client')
	actions_update_packet.apply('client')

def apply_server():
	s2c_hunger_update.apply('server')
	s2c_thirst_update.apply('server')
	packet.apply('server')
	actions_update_packet.apply('server')

__all__ = [apply_client.__name__, apply_server.__name__]
