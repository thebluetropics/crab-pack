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
	c_name = ['wb', 'nw'][side]

	cf = load_class_file(mod.config.path(f'stage/{side_name}/{c_name}.class'))
	cp_cache = cp_init_cache(cf[0x04])

	m = get_method(cf, cp_cache, ['d', 'c'][side], '(I)Z')
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = a_code_load(a[0x02])

	a_code[0x03] = assemble_code(cf, cp_cache, side, 0, [
		'iload_1',
		['getstatic', ('uu', 'na'), 'SOLID_GRASS_BLOCK', 'Lcom/thebluetropics/crabpack/SolidGrassBlock;'],
		['getfield', 'com/thebluetropics/crabpack/SolidGrassBlock', 'bn', 'I'],
		['if_icmpeq', 'a'],

		'iload_1',
		['getstatic', ('uu', 'na'), 'v', ('Lwp;', 'Loj;')],
		['getfield', ('wp', 'oj'), 'bn', 'I'],
		['if_icmpeq', 'a'],

		'iload_1',
		['getstatic', ('uu', 'na'), 'w', ('Luu;', 'Lna;')],
		['getfield', ('uu', 'na'), 'bn', 'I'],
		['if_icmpeq', 'a'],

		'iload_1',
		['getstatic', ('uu', 'na'), 'aB', ('Luu;', 'Lna;')],
		['getfield', ('uu', 'na'), 'bn', 'I'],
		['if_icmpne', 'b'],

		['label', 'a'],
		'iconst_1',
		['goto', 'c'],

		['label', 'b'],
		'iconst_0',

		['label', 'c'],
		'ireturn'
	])

	a_code[0x02] = len(a_code[0x03]).to_bytes(4)
	a_code[0x06] = (int.from_bytes(a_code[0x06]) - 1).to_bytes(2)

	for i, a in a_code[0x07]:
		if get_utf8_at(cp_cache, int.from_bytes(a[0x00])).__eq__('LineNumberTable'):
			del a_code[0x07][i]
			break

	a[0x02] = a_code_assemble(a_code)
	a[0x01] = len(a[0x02]).to_bytes(4)

	with open(mod.config.path(f'stage/{side_name}/{c_name}.class'), 'wb') as file:
		file.write(cf_assemble(cf))

	print(f'Patched {side_name}:{c_name}.class → net.minecraft.block.PlantBlock')
