import ctypes
import platform
import os
import mod

from sys import (exit, stderr)

def apply():
	lib_name = 'assets.dll' if platform.system().__eq__('Windows') else 'assets.so'
	lib_path = mod.config.path(f'lib/{lib_name}' if not mod.config.is_debug else f'c_libs/assets/lib/{lib_name}')

	if not os.path.exists(lib_path):
		print('Err: unknown.', file=stderr)
		exit(1)

	lib = ctypes.CDLL(lib_path)

	lib.apply_bottle.argtypes = [ctypes.c_char_p] * 2
	lib.apply_bottle.restype = ctypes.c_uint8

	lib.apply_cloth.argtypes = [ctypes.c_char_p] * 2
	lib.apply_cloth.restype = ctypes.c_uint8

	lib.apply_raw_squid_and_calamari.argtypes = [ctypes.c_char_p] * 3
	lib.apply_raw_squid_and_calamari.restype = ctypes.c_uint8

	lib.apply_fortress_bricks.argtypes = [ctypes.c_char_p] * 3
	lib.apply_fortress_bricks.restype = ctypes.c_uint8

	lib.apply_mortar.argtypes = [ctypes.c_char_p] * 5
	lib.apply_mortar.restype = ctypes.c_uint8

	lib.apply_hunger_and_thirst.argtypes = [ctypes.c_char_p] * 2
	lib.apply_hunger_and_thirst.restype = ctypes.c_uint8

	lib.apply_single_pixel_crosshair.argtypes = [ctypes.c_char_p] * 2
	lib.apply_single_pixel_crosshair.restype = ctypes.c_uint8

	if mod.config.is_feature_enabled('food.raw_squid_and_calamari'):
		ret_code = lib.apply_raw_squid_and_calamari(
			os.path.join(mod.config.path('assets'), 'raw_squid.png').encode('utf-8'),
			os.path.join(mod.config.path('assets'), 'calamari.png').encode('utf-8'),
			os.path.join(mod.config.path('stage'), 'client', 'gui', 'items.png').encode('utf-8'),
		)

		if not ret_code.__eq__(0):
			print('Err: unknown.', file=stderr)
			exit(1)

	if mod.config.is_feature_enabled('block.fortress_bricks'):
		ret_code = lib.apply_fortress_bricks(
			os.path.join(mod.config.path('assets'), 'fortress_bricks.png').encode('utf-8'),
			os.path.join(mod.config.path('assets'), 'light_fortress_bricks.png').encode('utf-8'),
			os.path.join(mod.config.path('stage'), 'client', 'terrain.png').encode('utf-8'),
		)

		if not ret_code.__eq__(0):
			print('Err: unknown.', file=stderr)
			exit(1)

	if mod.config.is_feature_enabled('block.mortar'):
		ret_code = lib.apply_mortar(
			os.path.join(mod.config.path('assets'), 'mortar_outer_top.png').encode('utf-8'),
			os.path.join(mod.config.path('assets'), 'mortar_inner_top.png').encode('utf-8'),
			os.path.join(mod.config.path('assets'), 'mortar_bottom.png').encode('utf-8'),
			os.path.join(mod.config.path('assets'), 'mortar_side.png').encode('utf-8'),
			os.path.join(mod.config.path('stage'), 'client', 'terrain.png').encode('utf-8'),
		)

		if not ret_code.__eq__(0):
			print('Err: unknown.', file=stderr)
			exit(1)

	if mod.config.is_feature_enabled('etc.hunger_and_thirst'):
		ret_code = lib.apply_hunger_and_thirst(
			os.path.join(mod.config.path('assets'), 'hunger_and_thirst.png').encode('utf-8'),
			os.path.join(mod.config.path('stage'), 'client', 'gui', 'icons.png').encode('utf-8'),
		)

		if not ret_code.__eq__(0):
			print('Err: unknown.', file=stderr)
			exit(1)

	if mod.config.is_feature_enabled('etc.hunger_and_thirst'):
		ret_code = lib.apply_bottle(
			os.path.join(mod.config.path('assets'), 'bottle.png').encode('utf-8'),
			os.path.join(mod.config.path('stage'), 'client', 'gui', 'items.png').encode('utf-8'),
		)

		if not ret_code.__eq__(0):
			print('Err: unknown.', file=stderr)
			exit(1)

	if mod.config.is_feature_enabled('experimental.cloth'):
		ret_code = lib.apply_cloth(
			os.path.join(mod.config.path('assets'), 'cloth.png').encode('utf-8'),
			os.path.join(mod.config.path('stage'), 'client', 'gui', 'items.png').encode('utf-8'),
		)

		if not ret_code.__eq__(0):
			print('Err: unknown.', file=stderr)
			exit(1)

	if mod.config.is_feature_enabled('user_interface.single_pixel_crosshair'):
		ret_code = lib.apply_single_pixel_crosshair(
			os.path.join(mod.config.path('assets'), 'single_pixel_crosshair.png').encode('utf-8'),
			os.path.join(mod.config.path('stage'), 'client', 'gui', 'icons.png').encode('utf-8'),
		)

		if not ret_code.__eq__(0):
			print('Err: unknown.', file=stderr)
			exit(1)
