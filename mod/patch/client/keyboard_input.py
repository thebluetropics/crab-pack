import mod

from modmaker.a import (
	get_attribute
)
from modmaker.a_code import (
	a_code_load,
	a_code_assemble,
	assemble_code
)
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
	if not mod.config.is_feature_enabled('debug.debug_fov'):
		return

	cf = load_class_file(mod.config.path('stage/client/lr.class'))
	cp_cache = cp_init_cache(cf[0x04])

	m = get_method(cf, cp_cache, 'a', '(IZ)V')
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = a_code_load(a[0x02])

	a_code[0x03] = assemble_code(cf, cp_cache, 0, 0, [
		'iload_1',
		['bipush', 41],
		['if_icmpne', 'a03'],

		'iload_2',
		['ifeq', 'a03'],

		['getstatic', 'px', 'useDebugFov', 'Z'],
		'iconst_1',
		'ixor',
		['putstatic', 'px', 'useDebugFov', 'Z'],
		'return',

		['label', 'a03']
	]) + a_code[0x03]

	a_code[0x02] = len(a_code[0x03]).to_bytes(4)
	a_code[0x06] = (int.from_bytes(a_code[0x06]) - 1).to_bytes(2)

	for i, a in a_code[0x07]:
		if get_utf8_at(cp_cache, int.from_bytes(a[0x00])).__eq__('LineNumberTable'):
			del a_code[0x07][i]
			break

	a[0x02] = a_code_assemble(a_code)
	a[0x01] = len(a[0x02]).to_bytes(4)

	with open(mod.config.path('stage/client/lr.class'), 'wb') as file:
		file.write(cf_assemble(cf))

	print('Patched client:lr.class → net.minecraft.client.input.KeyboardInput')
