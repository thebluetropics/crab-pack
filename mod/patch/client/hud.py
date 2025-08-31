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

	cf = class_file.load(mod.config.path('stage/client/uq.class'))
	xcp = constant_pool.use_helper(cf)

	m = get_method(cf, xcp, 'a', '(FZII)V')
	a = get_attribute(m[0x04], xcp, 'Code')

	a_code = attribute.code.load(a[0x02])

	a_code[0x01] = (26).to_bytes(2)
	a_code[0x03] = a_code[0x03][0:943] + instructions.assemble(0, [
		['sipush', 2929],
		['invokestatic', icpx_m(xcp, 'org/lwjgl/opengl/GL11', 'glDisable', '(I)V')], # → GL11.glEnable(GL11.GL_DEPTH_TEST)

    'aload_0',
    ['getfield', icpx_f(xcp, 'uq', 'g', 'Lnet/minecraft/client/Minecraft;')], # → this.minecraft
    ['getfield', icpx_f(xcp, 'net/minecraft/client/Minecraft', 'h', 'Ldc;')], # → this.minecraft.player
    ['getfield', icpx_f(xcp, 'dc', 'hunger', 'I')], # → int hunger
    'i2f',
    'aload_0',
    ['getfield', icpx_f(xcp, 'uq', 'g', 'Lnet/minecraft/client/Minecraft;')], # → this.minecraft
    ['getfield', icpx_f(xcp, 'net/minecraft/client/Minecraft', 'h', 'Ldc;')], # → this.minecraft.player
    ['getfield', icpx_f(xcp, 'dc', 'maxHunger', 'I')], # → int maxHunger
    'i2f',
    'fdiv',
		['bipush', 10],
		'i2f',
    'fmul',
		'f2i',
		['istore', 24],

		['bipush', 10],
		['iload', 24],
		'isub',
		['istore', 25],

		'aload_0',
		['iload', 6], 'iconst_2', 'idiv', ['bipush', 79], 'iadd', # → x0
		['iload', 7], ['bipush', 33], 'isub', # → y0
		['iload', 6], 'iconst_2', 'idiv', ['bipush', 90], 'iadd', # → x1
		['iload', 7], ['bipush', 23], ['iload', 24], ['iadd'], 'isub', # → y1
		['ldc_w', icpx_int(xcp, 0x40000000)], # → color
		['invokevirtual', icpx_m(xcp, 'uq', 'a', '(IIIII)V')], # → fill box for hunger (upper)

		# 00
		'aload_0',
		['iload', 6], 'iconst_2', 'idiv', ['bipush', 79], 'iadd', # → x0
		['iload', 7], ['bipush', 23], ['iload', 24], ['iadd'], 'isub', # → y0
		['iload', 6], 'iconst_2', 'idiv', ['bipush', 90], 'iadd', # → x1
		['iload', 7], ['bipush', 23], 'isub', # → y1
		['ldc_w', icpx_int(xcp, 0x40ff9966)], # → color
		['invokevirtual', icpx_m(xcp, 'uq', 'a', '(IIIII)V')], # → fill box for hunger (lower)

		# 00
		'aload_0',
		['iload', 6], 'iconst_2', 'idiv', ['bipush', 69], 'iadd', # → x0
		['iload', 7], ['bipush', 33], 'isub', # → y0
		['iload', 6], 'iconst_2', 'idiv', ['bipush', 77], 'iadd', # → x1
		['iload', 7],
		['bipush', 23], # → y1
		'isub',
		['ldc_w', icpx_int(xcp, 0x400099cc)],
		['invokevirtual', icpx_m(xcp, 'uq', 'a', '(IIIII)V')], # → fill box for thirst (lower)

		# 00
		'aload_0',
		['iload', 6],
		'iconst_2',
		'idiv',
		['bipush', 90], # → x0
		'iadd',
		['iload', 7],
		['bipush', 33], # → y0
		'isub',
		['iload', 6],
		'iconst_2',
		'idiv',
		['bipush', 91], # → x1
		'iadd',
		['iload', 7],
		['bipush', 23], # → y1
		'isub',
		['ldc_w', icpx_int(xcp, 0xff224400)], # color
		['invokevirtual', icpx_m(xcp, 'uq', 'a', '(IIIII)V')], # → fill box for hunger bar (background)

		# 00
		'aload_0',
		['iload', 6], 'iconst_2', 'idiv', ['bipush', 90], 'iadd', # → x0
		['iload', 7], ['bipush', 23], ['iload', 24], ['iadd'], 'isub',  # → y0
		['iload', 6], 'iconst_2', 'idiv', ['bipush', 91], 'iadd', # → x1
		['iload', 7], ['bipush', 23], 'isub', # → y1
		['ldc_w', icpx_int(xcp, 0xff33cc00)], # color
		['invokevirtual', icpx_m(xcp, 'uq', 'a', '(IIIII)V')], # → fill box for hunger bar (percentage)

		'aload_0',
		['iload', 6],
		'iconst_2',
		'idiv',
		['bipush', 77], # → x0
		'iadd',
		['iload', 7],
		['bipush', 33], # → y0
		'isub',
		['iload', 6],
		'iconst_2',
		'idiv',
		['bipush', 78], # → x1
		'iadd',
		['iload', 7],
		['bipush', 23], # → y1
		'isub',
		['ldc_w', icpx_int(xcp, 0xff004466)],
		['invokevirtual', icpx_m(xcp, 'uq', 'a', '(IIIII)V')], # → fill box for thirst bar (background)

		# 00
		'aload_0',
		['iload', 6], 'iconst_2', 'idiv', ['bipush', 77], 'iadd', # → x0
		['iload', 7], ['bipush', 33], 'isub', # → y0
		['iload', 6], 'iconst_2', 'idiv', ['bipush', 78], 'iadd', # → x1
		['iload', 7], ['bipush', 23], 'isub', # → y1
		['ldc_w', icpx_int(xcp, 0xff00ffff)], # color
		['invokevirtual', icpx_m(xcp, 'uq', 'a', '(IIIII)V')], # → fill box for thirst bar (percentage)

		'fconst_1',
		'fconst_1',
		'fconst_1',
		'fconst_1',
		['invokestatic', icpx_m(xcp, 'org/lwjgl/opengl/GL11', 'glColor4f', '(FFFF)V')],

		'aload_0',
		['iload', 6], 'iconst_2', 'idiv', ['bipush', 80], 'iadd', # → x
		['iload', 7], ['bipush', 33], 'isub', # → y
		['bipush', 16], # → u
		['bipush', 27], # → v
		['bipush', 10], # → width
		['iload', 25], # → height
		['invokevirtual', icpx_m(xcp, 'uq', 'b', '(IIIIII)V')],

		'aload_0',
		['iload', 6], 'iconst_2', 'idiv', ['bipush', 80], 'iadd', # → x
		['iload', 7], ['bipush', 33], 'isub', ['iload', 25], 'iadd', # → y
		['bipush', 26], # → u
		['bipush', 27], ['iload', 25], 'iadd', # → v
		['bipush', 10], # → width
		['iload', 24], # → height
		['invokevirtual', icpx_m(xcp, 'uq', 'b', '(IIIIII)V')],

		'aload_0',
		['iload', 6], 'iconst_2', 'idiv', ['bipush', 70], 'iadd', # → x
		['iload', 7], ['bipush', 33], 'isub', # → y
		['bipush', 23], # → u
		['bipush', 37], # → v
		['bipush', 7], # → width
		['bipush', 10], # → height
		['invokevirtual', icpx_m(xcp, 'uq', 'b', '(IIIIII)V')],

		['sipush', 2929],
		['invokestatic', icpx_m(xcp, 'org/lwjgl/opengl/GL11', 'glEnable', '(I)V')] # → GL11.glEnable(GL11.GL_DEPTH_TEST)
	]) + a_code[0x03][943:2102]

	# update code length
	a_code[0x02] = len(a_code[0x03]).to_bytes(4)

	# remove line number table
	a_code[0x06] = (int.from_bytes(a_code[0x06]) - 1).to_bytes(2)

	for i, a in a_code[0x07]:
		if get_utf8_at(xcp, int.from_bytes(a[0x00])).__eq__('LineNumberTable'):
			del a_code[0x07][i]
			break

	# update code attribute
	a[0x02] = attribute.code.assemble(a_code)

	# update code attribute length
	a[0x01] = len(a[0x02]).to_bytes(4)

	with open(mod.config.path('stage/client/uq.class'), 'wb') as f:
		f.write(class_file.assemble(cf))

	print('Patched client:uq.class → net.minecraft.client.gui.hud.InGameHud')
