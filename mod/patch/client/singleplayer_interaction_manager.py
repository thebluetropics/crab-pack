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
	if not mod.config.is_one_of_features_enabled(['actions']):
		return

	cf = load_class_file(mod.config.path('stage/client/os.class'))
	cp_cache = cp_init_cache(cf[0x04])

	_modify_break_block_method(cf, cp_cache)

	with open(mod.config.path('stage/client/os.class'), 'wb') as file:
		file.write(cf_assemble(cf))

	print('Patched client:os.class → net.minecraft.client.SingleplayerInteractionManager')

def _modify_break_block_method(cf, cp_cache):
	m = get_method(cf, cp_cache, 'b', '(IIII)Z')
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = a_code_load(a[0x02])

	a_code[0x03] = a_code[0x03][0:161] + assemble_code(cf, cp_cache, 0, 161, [
		*([] if not mod.config.is_feature_enabled('actions') else [
			'aload_0',
			['getfield', 'os', 'a', 'Lnet/minecraft/client/Minecraft;'], ['getfield', 'net/minecraft/client/Minecraft', 'h', 'Ldc;'],
			'iconst_1',
			['invokevirtual', 'gs', 'incrementActions', '(I)V'],
		])
	]) + a_code[0x03][161:164]

	a_code[0x02] = len(a_code[0x03]).to_bytes(4)
	a_code[0x06] = (int.from_bytes(a_code[0x06]) - 1).to_bytes(2)

	for i, a in a_code[0x07]:
		if get_utf8_at(cp_cache, int.from_bytes(a[0x00])).__eq__('LineNumberTable'):
			del a_code[0x07][i]
			break

	a[0x02] = a_code_assemble(a_code)
	a[0x01] = len(a[0x02]).to_bytes(4)
