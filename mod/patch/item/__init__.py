from . import (food_item, item)

def apply_client():
	food_item.apply_client()
	item.apply_client()

__all__ = [apply_client.__name__]
