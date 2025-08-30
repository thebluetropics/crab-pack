import mod

from mod.jvm import (
	class_file,
	attribute,
	instructions,
	constant_pool,
	get_method,
	get_attribute,
	icpx_c,
	icpx_f,
	icpx_m,
	icpx_string,
	get_utf8_at
)

def apply_client():
	if not mod.config.is_feature_enabled('fortress_bricks'):
		return

	cf = class_file.load(mod.config.path('stage/client/jy.class'))
	xcp = constant_pool.use_helper(cf)

	m = get_method(cf, xcp, 'a', '(Lhk;)V')
	a = get_attribute(m[0x04], xcp, 'Code')

	a_code = attribute.code.load(a[0x02])

	a_code[0x03] = a_code[0x03][0:178] + instructions.assemble(178, [
		'aload_1',
		['new', icpx_c(xcp, 'iz')],
		'dup',
		['getstatic', icpx_f(xcp, 'uu', 'fortress_bricks', 'Luu;')],
		['invokespecial', icpx_m(xcp, 'iz', '<init>', '(Luu;)V')],
		['bipush', 6],
		['anewarray', 7],
		'dup',
		'iconst_0',
		['ldc', icpx_string(xcp, 'ab')],
		'aastore',
		'dup',
		'iconst_1',
		['ldc',  icpx_string(xcp, 'ba')],
		'aastore',
		'dup',
		'iconst_2',
		['bipush', 97],
		['invokestatic', icpx_m(xcp, 'java/lang/Character', 'valueOf', '(C)Ljava/lang/Character;')],
		'aastore',
		'dup',
		'iconst_3',
		['getstatic', icpx_f(xcp, 'uu', 'x', 'Luu;')],
		'aastore',
		'dup',
		'iconst_4',
		['bipush', 98],
		['invokestatic', icpx_m(xcp, 'java/lang/Character', 'valueOf', '(C)Ljava/lang/Character;')],
		'aastore',
		'dup',
		'iconst_5',
		['getstatic', icpx_f(xcp, 'uu', 'u', 'Luu;')],
		'aastore',
		['invokevirtual', icpx_m(xcp, 'hk', 'a', '(Liz;[Ljava/lang/Object;)V')],
		'return'
	])
	a_code[0x02] = len(a_code[0x03]).to_bytes(4)

	# remove line number table
	a_code[0x06] = (int.from_bytes(a_code[0x06]) - 1).to_bytes(2)

	for i, a in a_code[0x07]:
		if get_utf8_at(xcp, int.from_bytes(a[0x00])).__eq__('LineNumberTable'):
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
	xcp = constant_pool.use_helper(cf)

	m = get_method(cf, xcp, 'a', '(Ley;)V')
	a = get_attribute(m[0x04], xcp, 'Code')

	a_code = attribute.code.load(a[0x02])

	a_code[0x03] = a_code[0x03][0:178] + instructions.assemble(178, [
		'aload_1',
		['new', icpx_c(xcp, 'fy')],
		'dup',
		['getstatic', icpx_f(xcp, 'na', 'fortress_bricks', 'Lna;')],
		['invokespecial', icpx_m(xcp, 'fy', '<init>', '(Lna;)V')],
		['bipush', 6],
		['anewarray', icpx_c(xcp, 'java/lang/Object')],
		'dup',
		'iconst_0',
		['ldc', icpx_string(xcp, 'ab')],
		'aastore',
		'dup',
		'iconst_1',
		['ldc', icpx_string(xcp, 'ba')],
		'aastore',
		'dup',
		'iconst_2',
		['bipush', 97],
		['invokestatic', icpx_m(xcp, 'java/lang/Character', 'valueOf', '(C)Ljava/lang/Character;')],
		'aastore',
		'dup',
		'iconst_3',
		['getstatic', icpx_f(xcp, 'na', 'x', 'Lna;')],
		'aastore',
		'dup',
		'iconst_4',
		['bipush', 98],
		['invokestatic', icpx_m(xcp, 'java/lang/Character', 'valueOf', '(C)Ljava/lang/Character;')],
		'aastore',
		'dup',
		'iconst_5',
		['getstatic', icpx_f(xcp, 'na', 'u', 'Lna;')],
		'aastore',
		['invokevirtual', icpx_m(xcp, 'ey', 'a', '(Lfy;[Ljava/lang/Object;)V')],
		'return'
	])

	# Update code length
	a_code[0x02] = len(a_code[0x03]).to_bytes(4)

	# remove line number table
	a_code[0x06] = (int.from_bytes(a_code[0x06]) - 1).to_bytes(2)

	for i, a in a_code[0x07]:
		if get_utf8_at(xcp, int.from_bytes(a[0x00])).__eq__('LineNumberTable'):
			del a_code[0x07][i]
			break

	# Update code attribute
	a[0x02] = attribute.code.assemble(a_code)

	# Update code attribute length
	a[0x01] = len(a[0x02]).to_bytes(4)

	with open(mod.config.path('stage/server/gp.class'), 'wb') as file:
		file.write(class_file.assemble(cf))

	print('Patched server:gp.class → net.minecraft.recipe.BlockRecipes')
