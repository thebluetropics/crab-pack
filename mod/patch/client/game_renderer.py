import mod

from modmaker.a import (
	get_attribute
)
from modmaker.a_code import (
	a_code_load,
	a_code_assemble,
	assemble_code
)
from modmaker.f import create_field
from modmaker.m import(
	get_method
)
from modmaker.cf import (
	load_class_file,
	cf_assemble
)
from modmaker.cp import (
	cp_init_cache,
	get_utf8_at
)

def apply():
	if not mod.config.is_one_of_features_enabled(['debug.debug_fov', 'debug.pause_prevention']):
		return

	cf = load_class_file(mod.config.path('stage/client/px.class'))
	cp_cache = cp_init_cache(cf[0x04])

	cf[0x0a] = (int.from_bytes(cf[0x0a]) + 1).to_bytes(2)
	cf[0x0b].append(create_field(cf, cp_cache, ['public', 'static'], 'useDebugFov', 'Z'))

	if mod.config.is_feature_enabled('debug.debug_fov'):
		_modify_static_initializer(cf, cp_cache)
		_modify_get_fov_method(cf, cp_cache)

	if mod.config.is_feature_enabled('debug.pause_prevention'):
		_modify_on_frame_update_method(cf, cp_cache)

	with open(mod.config.path('stage/client/px.class'), 'wb') as file:
		file.write(cf_assemble(cf))

	print('Patched client:px.class → net.minecraft.client.render.GameRenderer')

def _modify_static_initializer(cf, cp_cache):
	m = get_method(cf, cp_cache, '<clinit>', '()V')
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = a_code_load(a[0x02])

	a_code[0x03] = a_code[0x03][0:-1] + assemble_code(cf, cp_cache, 0, 0, [
		'iconst_0', ['putstatic', 'px', 'useDebugFov', 'Z'],
		'return'
	])

	a_code[0x02] = len(a_code[0x03]).to_bytes(4)

	a_code[0x06] = (int.from_bytes(a_code[0x06]) - 1).to_bytes(2)

	for i, a in a_code[0x07]:
		if get_utf8_at(cp_cache, int.from_bytes(a[0x00])).__eq__('LineNumberTable'):
			del a_code[0x07][i]
			break

	a[0x02] = a_code_assemble(a_code)
	a[0x01] = len(a[0x02]).to_bytes(4)

def _modify_get_fov_method(cf, cp_cache):
	m = get_method(cf, cp_cache, 'd', '(F)F')
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = a_code_load(a[0x02])

	a_code[0x03] = a_code[0x03][0:57] + assemble_code(cf, cp_cache, 0, 57, [
		['getstatic', 'px', 'useDebugFov', 'Z'],
		['ifeq', 'skip'],
		['bipush', 30],
		'i2f',
		'freturn',
		['label', 'skip']
	]) + a_code[0x03][57:76]

	a_code[0x02] = len(a_code[0x03]).to_bytes(4)
	a_code[0x06] = (int.from_bytes(a_code[0x06]) - 1).to_bytes(2)

	for i, a in a_code[0x07]:
		if get_utf8_at(cp_cache, int.from_bytes(a[0x00])).__eq__('LineNumberTable'):
			del a_code[0x07][i]
			break

	a[0x02] = a_code_assemble(a_code)
	a[0x01] = len(a[0x02]).to_bytes(4)

def _modify_on_frame_update_method(cf, cp_cache):
	m = get_method(cf, cp_cache, 'b', '(F)V')
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = a_code_load(a[0x02])
	a_code[0x03] = a_code[0x03][0:21] + assemble_code(cf, cp_cache, 0, 21, [
		'aload_0',
		['getfield', 'px', 'j', 'Lnet/minecraft/client/Minecraft;'],
		['invokevirtual', 'net/minecraft/client/Minecraft', 'h', '()V'],
	]) + a_code[0x03][28:len(a_code[0x03])]

	a_code[0x02] = len(a_code[0x03]).to_bytes(4)

	a_code[0x06] = (int.from_bytes(a_code[0x06]) - 1).to_bytes(2)

	for i, a in a_code[0x07]:
		if get_utf8_at(cp_cache, int.from_bytes(a[0x00])).__eq__('LineNumberTable'):
			del a_code[0x07][i]
			break

	a[0x02] = a_code_assemble(a_code)
	a[0x01] = len(a[0x02]).to_bytes(4)
