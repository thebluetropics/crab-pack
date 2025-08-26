from . import (block_recipes, smelting_recipe_manager)

def apply_client():
	block_recipes.apply_client()
	smelting_recipe_manager.apply_client()

__all__ = [apply_client.__name__]
