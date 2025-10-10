from modmaker import *
import mod

def apply():
	if not mod.config.is_one_of_features_enabled(['etc.hunger_and_thirst', 'actions']):
		return

	cf = load_class_file(mod.config.path('stage/client/uq.class'))
	cp_cache = cp_init_cache(cf[0x04])

	m = get_method(cf, cp_cache, 'a', '(FZII)V')
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = a_code_load(a[0x02])

	a_code[0x01] = (28).to_bytes(2)
	a_code[0x03] = a_code[0x03][0:943] + assemble_code(cf, cp_cache, 0, 0, [
		*([] if not mod.config.is_feature_enabled('etc.hunger_and_thirst') else [
			['sipush', 2929],
			['invokestatic', 'org/lwjgl/opengl/GL11', 'glDisable', '(I)V'],

			'aload_0',
			['getfield', 'uq', 'g', 'Lnet/minecraft/client/Minecraft;'],
			['getfield', 'net/minecraft/client/Minecraft', 'h', 'Ldc;'],
			['getfield', 'dc', 'hunger', 'I'],
			'i2f',
			'aload_0',
			['getfield', 'uq', 'g', 'Lnet/minecraft/client/Minecraft;'],
			['getfield', 'net/minecraft/client/Minecraft', 'h', 'Ldc;'],
			['getfield', 'dc', 'maxHunger', 'I'],
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
			['getfield', 'uq', 'g', 'Lnet/minecraft/client/Minecraft;'],
			['getfield', 'net/minecraft/client/Minecraft', 'h', 'Ldc;'],
			['getfield', 'dc', 'thirst', 'I'],
			'i2f',
			'aload_0',
			['getfield', 'uq', 'g', 'Lnet/minecraft/client/Minecraft;'],
			['getfield', 'net/minecraft/client/Minecraft', 'h', 'Ldc;'],
			['getfield', 'dc', 'maxThirst', 'I'],
			'i2f',
			'fdiv',
			['bipush', 10],
			'i2f',
			'fmul',
			'f2i',
			['istore', 26],

			['bipush', 10],
			['iload', 26],
			'isub',
			['istore', 27],

			'aload_0',
			['iload', 6], 'iconst_2', 'idiv', ['bipush', 79], 'iadd',
			['iload', 7], ['bipush', 33], 'isub',
			['iload', 6], 'iconst_2', 'idiv', ['bipush', 90], 'iadd',
			['iload', 7], ['bipush', 23], ['iload', 24], 'iadd', 'isub',
			['ldc_w.i32', 0x40000000],
			['invokevirtual', 'uq', 'a', '(IIIII)V'],

			'aload_0',
			['iload', 6], 'iconst_2', 'idiv', ['bipush', 79], 'iadd',
			['iload', 7], ['bipush', 23], ['iload', 24], 'iadd', 'isub',
			['iload', 6], 'iconst_2', 'idiv', ['bipush', 90], 'iadd',
			['iload', 7], ['bipush', 23], 'isub',
			['ldc_w.i32', 0x40ff9966],
			['invokevirtual', 'uq', 'a', '(IIIII)V'],

			'aload_0',
			['iload', 6], 'iconst_2', 'idiv', ['bipush', 69], 'iadd',
			['iload', 7], ['bipush', 33], 'isub',
			['iload', 6], 'iconst_2', 'idiv', ['bipush', 77], 'iadd',
			['iload', 7], ['bipush', 23], ['iload', 26], 'iadd', 'isub',
			['ldc_w.i32', 0x40000000],
			['invokevirtual', 'uq', 'a', '(IIIII)V'],

			'aload_0',
			['iload', 6], 'iconst_2', 'idiv', ['bipush', 69], 'iadd',
			['iload', 7], ['bipush', 23], ['iload', 26], 'iadd', 'isub',
			['iload', 6], 'iconst_2', 'idiv', ['bipush', 77], 'iadd',
			['iload', 7], ['bipush', 23], 'isub',
			['ldc_w.i32', 0x400099cc],
			['invokevirtual', 'uq', 'a', '(IIIII)V'],

			'aload_0',
			['iload', 6],
			'iconst_2',
			'idiv',
			['bipush', 90],
			'iadd',
			['iload', 7],
			['bipush', 33],
			'isub',
			['iload', 6],
			'iconst_2',
			'idiv',
			['bipush', 91],
			'iadd',
			['iload', 7],
			['bipush', 23],
			'isub',
			['ldc_w.i32', 0xff224400],
			['invokevirtual', 'uq', 'a', '(IIIII)V'],

			'aload_0',
			['iload', 6], 'iconst_2', 'idiv', ['bipush', 90], 'iadd',
			['iload', 7], ['bipush', 23], ['iload', 24], 'iadd', 'isub',
			['iload', 6], 'iconst_2', 'idiv', ['bipush', 91], 'iadd',
			['iload', 7], ['bipush', 23], 'isub',
			['ldc_w.i32', 0xff33cc00],
			['invokevirtual', 'uq', 'a', '(IIIII)V'],

			'aload_0',
			['iload', 6],
			'iconst_2',
			'idiv',
			['bipush', 77],
			'iadd',
			['iload', 7],
			['bipush', 33],
			'isub',
			['iload', 6],
			'iconst_2',
			'idiv',
			['bipush', 78],
			'iadd',
			['iload', 7],
			['bipush', 23],
			'isub',
			['ldc_w.i32', 0xff004466],
			['invokevirtual', 'uq', 'a', '(IIIII)V'],

			'aload_0',
			['iload', 6], 'iconst_2', 'idiv', ['bipush', 77], 'iadd',
			['iload', 7], ['bipush', 23], ['iload', 26], 'iadd', 'isub',
			['iload', 6], 'iconst_2', 'idiv', ['bipush', 78], 'iadd',
			['iload', 7], ['bipush', 23], 'isub',
			['ldc_w.i32', 0xff00ffff],
			['invokevirtual', 'uq', 'a', '(IIIII)V'],

			'fconst_1',
			'fconst_1',
			'fconst_1',
			'fconst_1',
			['invokestatic', 'org/lwjgl/opengl/GL11', 'glColor4f', '(FFFF)V'],

			'aload_0',
			['iload', 6], 'iconst_2', 'idiv', ['bipush', 80], 'iadd',
			['iload', 7], ['bipush', 33], 'isub',
			['bipush', 16],
			['bipush', 27],
			['bipush', 10],
			['iload', 25],
			['invokevirtual', 'uq', 'b', '(IIIIII)V'],

			'aload_0',
			['iload', 6], 'iconst_2', 'idiv', ['bipush', 70], 'iadd',
			['iload', 7], ['bipush', 33], 'isub',
			['bipush', 16],
			['bipush', 37],
			['bipush', 7],
			['iload', 27],
			['invokevirtual', 'uq', 'b', '(IIIIII)V'],

			'aload_0',
			['iload', 6], 'iconst_2', 'idiv', ['bipush', 80], 'iadd',
			['iload', 7], ['bipush', 33], 'isub', ['iload', 25], 'iadd',
			['bipush', 26],
			['bipush', 27], ['iload', 25], 'iadd',
			['bipush', 10],
			['iload', 24],
			['invokevirtual', 'uq', 'b', '(IIIIII)V'],

			'aload_0',
			['iload', 6], 'iconst_2', 'idiv', ['bipush', 70], 'iadd',
			['iload', 7], ['bipush', 33], 'isub', ['iload', 27], 'iadd',
			['bipush', 23],
			['bipush', 37], ['iload', 27], 'iadd',
			['bipush', 7],
			['iload', 26],
			['invokevirtual', 'uq', 'b', '(IIIIII)V'],

			['sipush', 2929],
			['invokestatic', 'org/lwjgl/opengl/GL11', 'glEnable', '(I)V']
		]),
		*([] if not mod.config.is_feature_enabled('actions') else [
			['getstatic', 'com/thebluetropics/crabpack/Actions', 'render', 'Z'],
			['ifeq', 'skip_render_actions'],

			'aload_0',
			['aload', 8],

			'aload_0',
			['getfield', 'uq', 'g', 'Lnet/minecraft/client/Minecraft;'],
			['getfield', 'net/minecraft/client/Minecraft', 'h', 'Ldc;'],
			['getfield', 'dc', 'actions', 'I'],
			['invokestatic', 'java/lang/Integer', 'toString', '(I)Ljava/lang/String;'],

			'iconst_0',
			'iconst_0',
			['ldc_w.i32', 0xffffff],
			['invokevirtual', 'uq', 'b', '(Lsj;Ljava/lang/String;III)V'],

			['label', 'skip_render_actions']
		])
	]) + a_code[0x03][943:2102]

	a_code[0x02] = len(a_code[0x03]).to_bytes(4)
	a_code[0x06] = (int.from_bytes(a_code[0x06]) - 1).to_bytes(2)

	for i, a in a_code[0x07]:
		if get_utf8_at(cp_cache, int.from_bytes(a[0x00])).__eq__('LineNumberTable'):
			del a_code[0x07][i]
			break

	a[0x02] = a_code_assemble(a_code)
	a[0x01] = len(a[0x02]).to_bytes(4)

	with open(mod.config.path('stage/client/uq.class'), 'wb') as file:
		file.write(cf_assemble(cf))

	print('Patched client:uq.class → net.minecraft.client.gui.hud.InGameHud')
