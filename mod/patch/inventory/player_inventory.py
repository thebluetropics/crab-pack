from modmaker import *
import mod

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

	for i, attribute in enumerate(a_code[0x07]):
		if get_utf8_at(cp_cache, int.from_bytes(attribute[0x00])).__eq__('LineNumberTable'):
			del a_code[0x07][i]
			break

	a_code[0x06] = len(a_code[0x07]).to_bytes(2)

	a[0x02] = a_code_assemble(a_code)
	a[0x01] = len(a[0x02]).to_bytes(4)

	with open(mod.config.path('stage/client/ix.class'), 'wb') as file:
		file.write(cf_assemble(cf))

	print('Patched client:ix.class → net.minecraft.inventory.PlayerInventory')
