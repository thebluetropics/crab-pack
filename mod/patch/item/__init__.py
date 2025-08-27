from . import (food_item, item)

def apply_client():
	food_item.apply_client()
	item.apply_client()

def apply_server():
	food_item.apply_server()
	item.apply_server()

__all__ = [apply_client.__name__]
