from . import (smelting_recipe_manager, crafting_recipe_manager)
import mod

def apply_client():
	smelting_recipe_manager.apply_client()
	if (
		mod.config.is_feature_enabled('block.fortress_bricks') or
		mod.config.is_feature_enabled('etc.hunger_and_thirst') or
		mod.config.is_feature_enabled('debug.debug_recipes') or
		mod.config.is_feature_enabled('block.mortar')
	):
		crafting_recipe_manager.apply('client')

def apply_server():
	smelting_recipe_manager.apply_server()
	if (
		mod.config.is_feature_enabled('block.fortress_bricks') or
		mod.config.is_feature_enabled('etc.hunger_and_thirst') or
		mod.config.is_feature_enabled('debug.debug_recipes') or
		mod.config.is_feature_enabled('block.mortar')
	):
		crafting_recipe_manager.apply('server')

__all__ = [apply_client.__name__]
