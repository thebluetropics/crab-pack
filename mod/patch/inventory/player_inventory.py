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

def apply_client():
	if not mod.config.is_feature_enabled('zoom'):
		return

	cf = load_class_file(mod.config.path('stage/client/ix.class'))
	cp_cache = cp_init_cache(cf[0x04])

	m = get_method(cf, cp_cache, 'b', '(I)V')
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = a_code_load(a[0x02])

	a_code[0x03] = assemble_code(cf, cp_cache, 0, 0, [
		'iload_1',
		['invokestatic', 'com/thebluetropics/crabpack/Zoom', 'onMouseScroll', '(I)Z'],
		['ifeq', 'skip'],
		'return',

		['label', 'skip']
	]) + a_code[0x03]

	a_code[0x02] = len(a_code[0x03]).to_bytes(4)
	a_code[0x06] = (int.from_bytes(a_code[0x06]) - 1).to_bytes(2)

	for i, a in a_code[0x07]:
		if get_utf8_at(cp_cache, int.from_bytes(a[0x00])).__eq__('LineNumberTable'):
			del a_code[0x07][i]
			break

	a[0x02] = a_code_assemble(a_code)
	a[0x01] = len(a[0x02]).to_bytes(4)

	with open(mod.config.path('stage/client/ix.class'), 'wb') as file:
		file.write(cf_assemble(cf))

	print('Patched client:ix.class → net.minecraft.inventory.PlayerInventory')
