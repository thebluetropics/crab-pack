from . import (
	s2c_update_hunger
)

def apply_client():
	s2c_update_hunger.apply_client()

def apply_server():
	pass

__all__ = [apply_client.__name__, apply_server.__name__]
