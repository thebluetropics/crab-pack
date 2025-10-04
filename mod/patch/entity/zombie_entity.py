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
	create_method
)
from modmaker.cf import (
	load_class_file,
	cf_assemble
)
from modmaker.cp import (
	cp_init_cache,
	i2cpx_utf8
)

def apply(side_name):
	if not mod.config.is_feature_enabled('item.cloth'):
		pass

	side = 0 if side_name.__eq__('client') else 1
	c_name = ['uz', 'ne'][side]

	cf = load_class_file(mod.config.path(f'stage/{side_name}/{c_name}.class'))
	cp_cache = cp_init_cache(cf[0x04])

	cf[0x0d].append(_create_drop_items_method(cf, cp_cache, side, c_name))
	cf[0x0c] = len(cf[0x0d]).to_bytes(2)

	with open(mod.config.path(f'stage/{side_name}/{c_name}.class'), 'wb') as file:
		file.write(cf_assemble(cf))

	print(f'Patched {side_name}:{c_name}.class → net.minecraft.entity.ZombieEntity')

def _create_drop_items_method(cf, cp_cache, side, c_name):
	m = create_method(cf, cp_cache, ['protected'], 'q', '()V')

	code = assemble_code(cf, cp_cache, side, 0, [
		'aload_0', ['getfield', c_name, ('bs', 'bv'), 'Ljava/util/Random;'],
		'iconst_2',
		['invokevirtual', 'java/util/Random', 'nextInt', '(I)I'],
		['ifeq', 'skip'],

		'aload_0',
		['getstatic', ('gm', 'ej'), 'CLOTH', ('Lgm;', 'Lej;')],
		['getfield', ('gm', 'ej'), 'bf', 'I'],
		'iconst_1',
		['invokevirtual', c_name, 'b', ('(II)Lhl;', '(II)Lez;')],
		'pop',

		['label', 'skip'],
		'return'
	])
	a_code = a_code_assemble([
		(3).to_bytes(2),
		(1).to_bytes(2),
		len(code).to_bytes(4),
		code,
		(0).to_bytes(2),
		[],
		(0).to_bytes(2),
		[]
	])
	a = [i2cpx_utf8(cf, cp_cache, 'Code'), len(a_code).to_bytes(4), a_code]

	m[0x03] = (1).to_bytes(2)
	m[0x04] = [a]

	return m
