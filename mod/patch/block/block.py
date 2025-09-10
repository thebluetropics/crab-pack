import mod

from mod.attribute import get_attribute
from mod.field import create_field
from mod.method import get_method
from mod import (
	class_file,
	attribute,
	instructions,
	constant_pool
)
from mod.constant_pool import (
	icpx_c,
	icpx_f,
	icpx_m,
	icpx_string,
	get_utf8_at
)

def apply(side_name):
	if not mod.config.is_feature_enabled('block.fortress_bricks'):
		return

	side = 0 if side_name.__eq__('client') else 1
	c_name = ['uu', 'na'][side]

	cf = class_file.load(mod.config.path(f'stage/{side_name}/{c_name}.class'))
	cp_cache = constant_pool.init_constant_pool_cache(cf[0x04])

	cf[0x0a] = (int.from_bytes(cf[0x0a]) + 1).to_bytes(2)
	cf[0x0b].append(create_field(cf, cp_cache, ['public', 'static'], 'fortress_bricks', f'L{c_name};'))

	_patch_static_initializer(cf, cp_cache, side, c_name)

	with open(mod.config.path(f'stage/{side_name}/{c_name}.class'), 'wb') as file:
		file.write(class_file.assemble(cf))

	print(f'Patched {side_name}:{c_name}.class → net.minecraft.block.Block')

def _patch_static_initializer(cf, cp_cache, side, c_name):
	m = get_method(cf, cp_cache, '<clinit>', '()V')
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = attribute.code.load(a[0x02])

	a_code[0x03] = a_code[0x03][0:3398] + instructions.assemble(3398, [
		['new', icpx_c(cf, cp_cache, c_name)],
		'dup',
		['bipush', 97],
		['sipush', 166],
		['getstatic', icpx_f(cf, cp_cache, ['ln', 'hj'][side], 'e', ['Lln;', 'Lhj;'][side])],
		['invokespecial', icpx_m(cf, cp_cache, c_name, '<init>', ['(IILln;)V', '(IILhj;)V'][side])],
		'fconst_2',
		['invokevirtual', icpx_m(cf, cp_cache, c_name, 'c', ['(F)Luu;', '(F)Lna;'][side])],
		['ldc', 22],
		['invokevirtual', icpx_m(cf, cp_cache, c_name, 'b', ['(F)Luu;', '(F)Lna;'][side])],
		['getstatic', icpx_f(cf, cp_cache, c_name, 'h', ['Lct;', 'Lbu;'][side])],
		['invokevirtual', icpx_m(cf, cp_cache, c_name, 'a', ['(Lct;)Luu;', '(Lbu;)Lna;'][side])],
		['ldc_w', icpx_string(cf, cp_cache, 'fortress_bricks')],
		['invokevirtual', icpx_m(cf, cp_cache, c_name, 'a', ['(Ljava/lang/String;)Luu;', '(Ljava/lang/String;)Lna;'][side])],
		['putstatic', icpx_f(cf, cp_cache, c_name, 'fortress_bricks', ['Luu;', 'Lna;'][side])]
	]) + a_code[0x03][3398:3678]
	a_code[0x02] = len(a_code[0x03]).to_bytes(4)

	# remove line number table
	a_code[0x06] = (int.from_bytes(a_code[0x06]) - 1).to_bytes(2)

	for i, a in a_code[0x07]:
		if get_utf8_at(cp_cache, int.from_bytes(a[0x00])).__eq__('LineNumberTable'):
			del a[0x07][i]
			break

	# update code attribute
	a[0x02] = attribute.code.assemble(a_code)

	# update code attribute length
	a[0x01] = len(a[0x02]).to_bytes(4)
