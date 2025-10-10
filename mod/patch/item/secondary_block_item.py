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

def apply(side_name):
	if not mod.config.is_feature_enabled('blackbox'):
		return

	side = 0 if side_name.__eq__('client') else 1
	c_name = ['lv', 'hn'][side]

	cf = load_class_file(mod.config.path(f'stage/{side_name}/{c_name}.class'))
	cp_cache = cp_init_cache(cf[0x04])

	_modify_use_on_block_method(cf, cp_cache, side)

	with open(mod.config.path(f'stage/{side_name}/{c_name}.class'), 'wb') as file:
		file.write(cf_assemble(cf))

	print(f'Patched {side_name}:{c_name}.class → net.minecraft.item.SecondaryBlockItem')

def _modify_use_on_block_method(cf, cp_cache, side):
	m = get_method(cf, cp_cache, 'a', ['(Liz;Lgs;Lfd;IIII)Z', '(Lfy;Lem;Ldj;IIII)Z'][side])
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = a_code_load(a[0x02])

	code = assemble_code(cf, cp_cache, side, 239, [
		'aload_3', ['getfield', ('fd', 'dj'), 'B', 'Z'], ['ifne', 'skip'],

		['getstatic', 'com/thebluetropics/crabpack/Blackbox', 'INSTANCE', 'Lcom/thebluetropics/crabpack/Blackbox;'],
		'aload_2', ['getfield', ('gs', 'em'), ('l', 'r'), 'Ljava/lang/String;'],
		['iload', 4], ['iload', 5], ['iload', 6],
		'aload_3', ['iload', 4], ['iload', 5], ['iload', 6], ['invokevirtual', ('fd', 'dj'), 'a', '(III)I'],
		'aload_3', ['iload', 4], ['iload', 5], ['iload', 6], ['invokevirtual', ('fd', 'dj'), ('e', 'c'), '(III)I'],
		['invokevirtual', 'com/thebluetropics/crabpack/Blackbox', 'onPlaceBlock', '(Ljava/lang/String;IIIII)V'],

		['label', 'skip']
	])

	a_code[0x03] = a_code[0x03][0:105] + (
		(int.from_bytes(a_code[0x03][105:107], signed=True) + len(code)).to_bytes(2, signed=True)
	) + a_code[0x03][107:132] + (
		(int.from_bytes(a_code[0x03][132:134], signed=True) + len(code)).to_bytes(2, signed=True)
	) + a_code[0x03][134:239] + code + a_code[0x03][239:241]

	a_code[0x02] = len(a_code[0x03]).to_bytes(4)
	a_code[0x06] = (int.from_bytes(a_code[0x06]) - 1).to_bytes(2)

	for i, a in a_code[0x07]:
		if get_utf8_at(cp_cache, int.from_bytes(a[0x00])).__eq__('LineNumberTable'):
			del a_code[0x07][i]
			break

	a[0x02] = a_code_assemble(a_code)
	a[0x01] = len(a[0x02]).to_bytes(4)
