import mod

from mod.attribute import get_attribute
from mod.method import get_method
from mod.constant_pool import get_utf8_at
from mod import (
	class_file,
	attribute,
	constant_pool,
	instructions
)
from mod.constant_pool import (
	icpx_f,
	icpx_m
)

def apply(side_name):
	if not mod.config.is_feature_enabled('block.solid_grass_block'):
		return

	side = 0 if side_name.__eq__('client') else 1
	c_name = ['km', 'gu'][side]

	cf = class_file.load(mod.config.path(f'stage/{side_name}/{c_name}.class'))
	cp_cache = constant_pool.init_constant_pool_cache(cf[0x04])

	_modify_use_on_block_method(cf, cp_cache, side)

	with open(mod.config.path(f'stage/{side_name}/{c_name}.class'), 'wb') as file:
		file.write(class_file.assemble(cf))

	print(f'Patched {side_name}:{c_name}.class → net.minecraft.item.DyeItem')

def _modify_use_on_block_method(cf, cp_cache, side):
	m = get_method(cf, cp_cache, 'a', ['(Liz;Lgs;Lfd;IIII)Z', '(Lfy;Lem;Ldj;IIII)Z'][side])
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = attribute.code.load(a[0x02])

	a_code[0x03] = instructions.assemble(0, [
		['aload', 3],
		['iload', 4],
		['iload', 5],
		['iload', 6],
		['invokevirtual', icpx_m(cf, cp_cache, ['fd', 'dj'][side], 'a', '(III)I')],
		['getstatic', icpx_f(cf, cp_cache, ['uu', 'na'][side], 'v', ['Lwp;', 'Loj;'][side])],
		['getfield', icpx_f(cf, cp_cache, ['wp', 'oj'][side], 'bn', 'I')],
		['if_icmpne*', 'a'],

		['aload', 3],
		['getfield', icpx_f(cf, cp_cache, ['fd', 'dj'][side], 'B', 'Z')],
		['ifne*', 'b'],

		['aload', 3],
		['iload', 4],
		['iload', 5],
		['iload', 6],
		['getstatic', icpx_f(cf, cp_cache, ['uu', 'na'][side], 'SOLID_GRASS_BLOCK', 'Lcom/thebluetropics/crabpack/SolidGrassBlock;')],
		['getfield', icpx_f(cf, cp_cache, ['uu', 'na'][side], 'bn', 'I')],
		['invokevirtual', icpx_m(cf, cp_cache, ['fd', 'dj'][side], ['f', 'e'][side], '(IIII)Z')],
		'pop',

		['aload', 1],
		['dup'],
		['getfield', icpx_f(cf, cp_cache, ['iz', 'fy'][side], 'a', 'I')],
		'iconst_1',
		'isub',
		['putfield', icpx_f(cf, cp_cache, ['iz', 'fy'][side], 'a', 'I')],

		['jump_target*', 'a'],
		'iconst_1',
		'ireturn',

		['jump_target*', 'b']
	]) + a_code[0x03][0:380]
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
