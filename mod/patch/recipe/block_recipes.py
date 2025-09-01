import mod

from mod.attribute import get_attribute
from mod.method import get_method
from mod import (
	class_file,
	attribute,
	instructions,
	constant_pool
)
from mod.constant_pool import (
	icpx_f,
	icpx_m,
	get_utf8_at,
	icpx_string,
	icpx_c
)

def apply_client():
	if not mod.config.is_feature_enabled('fortress_bricks'):
		return

	cf = class_file.load(mod.config.path('stage/client/jy.class'))
	cp_cache = constant_pool.init_constant_pool_cache(cf[0x04])

	m = get_method(cf, cp_cache, 'a', '(Lhk;)V')
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = attribute.code.load(a[0x02])

	a_code[0x03] = a_code[0x03][0:178] + instructions.assemble(178, [
		'aload_1',
		['new', icpx_c(cf, cp_cache, 'iz')],
		'dup',
		['getstatic', icpx_f(cf, cp_cache, 'uu', 'fortress_bricks', 'Luu;')],
		['invokespecial', icpx_m(cf, cp_cache, 'iz', '<init>', '(Luu;)V')],
		['bipush', 6],
		['anewarray', 7],
		'dup',
		'iconst_0',
		['ldc', icpx_string(cf, cp_cache, 'ab')],
		'aastore',
		'dup',
		'iconst_1',
		['ldc',  icpx_string(cf, cp_cache, 'ba')],
		'aastore',
		'dup',
		'iconst_2',
		['bipush', 97],
		['invokestatic', icpx_m(cf, cp_cache, 'java/lang/Character', 'valueOf', '(C)Ljava/lang/Character;')],
		'aastore',
		'dup',
		'iconst_3',
		['getstatic', icpx_f(cf, cp_cache, 'uu', 'x', 'Luu;')],
		'aastore',
		'dup',
		'iconst_4',
		['bipush', 98],
		['invokestatic', icpx_m(cf, cp_cache, 'java/lang/Character', 'valueOf', '(C)Ljava/lang/Character;')],
		'aastore',
		'dup',
		'iconst_5',
		['getstatic', icpx_f(cf, cp_cache, 'uu', 'u', 'Luu;')],
		'aastore',
		['invokevirtual', icpx_m(cf, cp_cache, 'hk', 'a', '(Liz;[Ljava/lang/Object;)V')],
		'return'
	])
	a_code[0x02] = len(a_code[0x03]).to_bytes(4)

	# remove line number table
	a_code[0x06] = (int.from_bytes(a_code[0x06]) - 1).to_bytes(2)

	for i, a in a_code[0x07]:
		if get_utf8_at(cp_cache, int.from_bytes(a[0x00])).__eq__('LineNumberTable'):
			del a_code[0x07][i]
			break

	# Update code attribute
	a[0x02] = attribute.code.assemble(a_code)

	# Update code attribute length
	a[0x01] = len(a[0x02]).to_bytes(4)

	with open(mod.config.path('stage/client/jy.class'), 'wb') as f:
		f.write(class_file.assemble(cf))

	print('Patched client:jy.class → net.minecraft.recipe.BlockRecipes')

def apply_server():
	if not mod.config.is_feature_enabled('fortress_bricks'):
		return

	cf = class_file.load(mod.config.path('stage/server/gp.class'))
	cp_cache = constant_pool.init_constant_pool_cache(cf[0x04])

	m = get_method(cf, cp_cache, 'a', '(Ley;)V')
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = attribute.code.load(a[0x02])

	a_code[0x03] = a_code[0x03][0:178] + instructions.assemble(178, [
		'aload_1',
		['new', icpx_c(cf, cp_cache, 'fy')],
		'dup',
		['getstatic', icpx_f(cf, cp_cache, 'na', 'fortress_bricks', 'Lna;')],
		['invokespecial', icpx_m(cf, cp_cache, 'fy', '<init>', '(Lna;)V')],
		['bipush', 6],
		['anewarray', icpx_c(cf, cp_cache, 'java/lang/Object')],
		'dup',
		'iconst_0',
		['ldc', icpx_string(cf, cp_cache, 'ab')],
		'aastore',
		'dup',
		'iconst_1',
		['ldc', icpx_string(cf, cp_cache, 'ba')],
		'aastore',
		'dup',
		'iconst_2',
		['bipush', 97],
		['invokestatic', icpx_m(cf, cp_cache, 'java/lang/Character', 'valueOf', '(C)Ljava/lang/Character;')],
		'aastore',
		'dup',
		'iconst_3',
		['getstatic', icpx_f(cf, cp_cache, 'na', 'x', 'Lna;')],
		'aastore',
		'dup',
		'iconst_4',
		['bipush', 98],
		['invokestatic', icpx_m(cf, cp_cache, 'java/lang/Character', 'valueOf', '(C)Ljava/lang/Character;')],
		'aastore',
		'dup',
		'iconst_5',
		['getstatic', icpx_f(cf, cp_cache, 'na', 'u', 'Lna;')],
		'aastore',
		['invokevirtual', icpx_m(cf, cp_cache, 'ey', 'a', '(Lfy;[Ljava/lang/Object;)V')],
		'return'
	])

	# Update code length
	a_code[0x02] = len(a_code[0x03]).to_bytes(4)

	# remove line number table
	a_code[0x06] = (int.from_bytes(a_code[0x06]) - 1).to_bytes(2)

	for i, a in a_code[0x07]:
		if get_utf8_at(cp_cache, int.from_bytes(a[0x00])).__eq__('LineNumberTable'):
			del a_code[0x07][i]
			break

	# Update code attribute
	a[0x02] = attribute.code.assemble(a_code)

	# Update code attribute length
	a[0x01] = len(a[0x02]).to_bytes(4)

	with open(mod.config.path('stage/server/gp.class'), 'wb') as file:
		file.write(class_file.assemble(cf))

	print('Patched server:gp.class → net.minecraft.recipe.BlockRecipes')
