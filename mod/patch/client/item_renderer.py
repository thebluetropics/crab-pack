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
	icpx_int,
	get_utf8_at
)

def apply():
	if not mod.config.is_feature_enabled('hunger_and_thirst'):
		return

	cf = class_file.load(mod.config.path('stage/client/bb.class'))
	cp_cache = constant_pool.init_constant_pool_cache(cf[0x04])

	_modify_render_item_decoration_method(cf, cp_cache)

	with open(mod.config.path('stage/client/bb.class'), 'wb') as f:
		f.write(class_file.assemble(cf))

	print('Patched client:bb.class → net.minecraft.client.render.ItemRenderer')

def _modify_render_item_decoration_method(cf, cp_cache):
	m = get_method(cf, cp_cache, 'b', '(Lsj;Lji;Liz;II)V')
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = attribute.code.load(a[0x02])
	const = {
		'GL_LIGHTING': 2896,
		'GL_DEPTH_TEST': 2929,
		'GL_TEXTURE_2D': 3553
	}

	a_code[0x01] = (13).to_bytes(2)
	a_code[0x03] = a_code[0x03][0:288] + instructions.assemble(0, [
		['aload', 3],
		['ifnull*', 'end'],

		['aload', 3],
		['invokevirtual', icpx_m(cf, cp_cache, 'iz', 'a', '()Lgm;')],
		['getstatic', icpx_f(cf, cp_cache, 'gm', 'BOTTLE', 'Lgm;')],
		['if_acmpne*', 'end'],

		['aload', 3],
		['invokevirtual', icpx_m(cf, cp_cache, 'iz', 'i', '()I')],
		['bipush', 100],
		['if_icmpge*', 'end'],

		['aload', 3],
		['invokevirtual', icpx_m(cf, cp_cache, 'iz', 'i', '()I')],
		'i2f',
		['sipush', 100],
		'i2f',
		'fdiv',
		['bipush', 13],
		'i2f',
		'fmul',
		['invokestatic', icpx_m(cf, cp_cache, 'java/lang/Math', 'round', '(F)I')],
		['istore', 12],

		['sipush', const['GL_LIGHTING']],
		['invokestatic', icpx_m(cf, cp_cache, 'org/lwjgl/opengl/GL11', 'glDisable', '(I)V')],
		['sipush', const['GL_DEPTH_TEST']],
		['invokestatic', icpx_m(cf, cp_cache, 'org/lwjgl/opengl/GL11', 'glDisable', '(I)V')],
		['sipush', const['GL_TEXTURE_2D']],
		['invokestatic', icpx_m(cf, cp_cache, 'org/lwjgl/opengl/GL11', 'glDisable', '(I)V')],

		['getstatic', icpx_f(cf, cp_cache, 'nw', 'a', 'Lnw;')],
		['astore', 8],

		['aload', 0],
		['aload', 8],
		['iload', 4], 'iconst_2', 'iadd',
		['iload', 5], ['bipush', 13], 'iadd',
		['bipush', 13],
		'iconst_2',
		'iconst_0',
		['invokevirtual', icpx_m(cf, cp_cache, 'bb', 'a', '(Lnw;IIIII)V')],

		['aload', 0],
		['aload', 8],
		['iload', 4], 'iconst_2', 'iadd',
		['iload', 5], ['bipush', 13], 'iadd',
		['iload', 12],
		'iconst_1',
		['ldc_w', icpx_int(cf, cp_cache, 0xff66cccc)],
		['invokevirtual', icpx_m(cf, cp_cache, 'bb', 'a', '(Lnw;IIIII)V')],

		['sipush', 3553],
		['invokestatic', icpx_m(cf, cp_cache, 'org/lwjgl/opengl/GL11', 'glEnable', '(I)V')],
		['sipush', 2896],
		['invokestatic', icpx_m(cf, cp_cache, 'org/lwjgl/opengl/GL11', 'glEnable', '(I)V')],
		['sipush', 2929],
		['invokestatic', icpx_m(cf, cp_cache, 'org/lwjgl/opengl/GL11', 'glEnable', '(I)V')],

		'fconst_1',
		'fconst_1',
		'fconst_1',
		'fconst_1',
		['invokestatic', icpx_m(cf, cp_cache, 'org/lwjgl/opengl/GL11', 'glColor4f', '(FFFF)V')],

		['jump_target*', 'end'],
		'return'
	])
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
