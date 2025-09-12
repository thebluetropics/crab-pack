import mod

from mod.attribute import get_attribute
from mod.method import get_method
from mod import (
	attribute,
	instructions,
	constant_pool
)
from mod.class_file import (
	load_class_file,
	assemble_class_file
)
from mod.constant_pool import (
	get_utf8_at,
	icpx_f
)

def apply(side_name):
	if not mod.config.is_feature_enabled('block.solid_grass_block'):
		return

	side = 0 if side_name.__eq__('client') else 1
	c_name = ['wb', 'nw'][side]

	cf = load_class_file(mod.config.path(f'stage/{side_name}/{c_name}.class'))
	cp_cache = constant_pool.init_constant_pool_cache(cf[0x04])

	m = get_method(cf, cp_cache, ['d', 'c'][side], '(I)Z')
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = attribute.code.load(a[0x02])

	a_code[0x03] = instructions.assemble(0, [
		['iload', 1],
		['getstatic', icpx_f(cf, cp_cache, ['uu', 'na'][side], 'SOLID_GRASS_BLOCK', 'Lcom/thebluetropics/crabpack/SolidGrassBlock;')],
		['getfield', icpx_f(cf, cp_cache, 'com/thebluetropics/crabpack/SolidGrassBlock', 'bn', 'I')],
		['if_icmpeq*', 'a'],

		['iload', 1],
		['getstatic', icpx_f(cf, cp_cache, ['uu', 'na'][side], 'v', ['Lwp;', 'Loj;'][side])],
		['getfield', icpx_f(cf, cp_cache, ['wp', 'oj'][side], 'bn', 'I')],
		['if_icmpeq*', 'a'],

		['iload', 1],
		['getstatic', icpx_f(cf, cp_cache, ['uu', 'na'][side], 'w', ['Luu;', 'Lna;'][side])],
		['getfield', icpx_f(cf, cp_cache, ['uu', 'na'][side], 'bn', 'I')],
		['if_icmpeq*', 'a'],

		['iload', 1],
		['getstatic', icpx_f(cf, cp_cache, ['uu', 'na'][side], 'aB', ['Luu;', 'Lna;'][side])],
		['getfield', icpx_f(cf, cp_cache, ['uu', 'na'][side], 'bn', 'I')],
		['if_icmpne*', 'b'],

		['jump_target*', 'a'],
		'iconst_1',
		['goto*', 'c'],

		['jump_target*', 'b'],
		'iconst_0',

		['jump_target*', 'c'],
		'ireturn'
	])

	# update code length
	a_code[0x02] = len(a_code[0x03]).to_bytes(4)

	# remove line number table
	a_code[0x06] = (int.from_bytes(a_code[0x06]) - 1).to_bytes(2)

	for i, a in a_code[0x07]:
		if get_utf8_at(cp_cache, int.from_bytes(a[0x00])).__eq__('LineNumberTable'):
			del a_code[0x07][i]
			break

	# update code attribute
	a[0x02] = attribute.code.assemble(a_code)

	# update code attribute length
	a[0x01] = len(a[0x02]).to_bytes(4)

	with open(mod.config.path(f'stage/{side_name}/{c_name}.class'), 'wb') as file:
		file.write(assemble_class_file(cf))

	print(f'Patched {side_name}:{c_name}.class → net.minecraft.block.PlantBlock')
