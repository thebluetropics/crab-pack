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
	if not mod.config.is_feature_enabled('block.solid_grass_block'):
		return

	side = 0 if side_name.__eq__('client') else 1
	c_name = ['km', 'gu'][side]

	cf = load_class_file(mod.config.path(f'stage/{side_name}/{c_name}.class'))
	cp_cache = cp_init_cache(cf[0x04])

	_modify_use_on_block_method(cf, cp_cache, side)

	with open(mod.config.path(f'stage/{side_name}/{c_name}.class'), 'wb') as file:
		file.write(cf_assemble(cf))

	print(f'Patched {side_name}:{c_name}.class → net.minecraft.item.DyeItem')

def _modify_use_on_block_method(cf, cp_cache, side):
	m = get_method(cf, cp_cache, 'a', ['(Liz;Lgs;Lfd;IIII)Z', '(Lfy;Lem;Ldj;IIII)Z'][side])
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = a_code_load(a[0x02])

	a_code[0x03] = assemble_code(cf, cp_cache, side, 0, [
		['aload', 3],
		['iload', 4],
		['iload', 5],
		['iload', 6],
		['invokevirtual', ('fd', 'dj'), 'a', '(III)I'],
		['getstatic', ('uu', 'na'), 'v', ('Lwp;', 'Loj;')],
		['getfield', ('wp', 'oj'), 'bn', 'I'],
		['if_icmpne', 'a'],

		['aload', 3],
		['getfield', ('fd', 'dj'), 'B', 'Z'],
		['ifne', 'a'],

		['aload', 3],
		['iload', 4],
		['iload', 5],
		['iload', 6],
		['getstatic', ('uu', 'na'), 'SOLID_GRASS_BLOCK', 'Lcom/thebluetropics/crabpack/SolidGrassBlock;'],
		['getfield', ('uu', 'na'), 'bn', 'I'],
		['invokevirtual', ('fd', 'dj'), ('f', 'e'), '(IIII)Z'],
		'pop',

		['aload', 1],
		'dup',
		['getfield', ('iz', 'fy'), 'a', 'I'],
		'iconst_1',
		'isub',
		['putfield', ('iz', 'fy'), 'a', 'I'],

		'iconst_1',
		'ireturn',

		['label', 'a']
	]) + a_code[0x03][0:380]
	a_code[0x02] = len(a_code[0x03]).to_bytes(4)

	# remove line number table
	a_code[0x06] = (int.from_bytes(a_code[0x06]) - 1).to_bytes(2)

	for i, a in a_code[0x07]:
		if get_utf8_at(cp_cache, int.from_bytes(a[0x00])).__eq__('LineNumberTable'):
			del a_code[0x07][i]
			break

	# update code attribute
	a[0x02] = a_code_assemble(a_code)

	# update code attribute length
	a[0x01] = len(a[0x02]).to_bytes(4)
