from modmaker import *
import mod, struct

def apply():
	if not mod.config.is_feature_enabled('etc.hunger_and_thirst'):
		return

	cf = load_class_file(mod.config.path('stage/client/bb.class'))
	cp_cache = cp_init_cache(cf[0x04])

	_modify_render_item_decoration_method(cf, cp_cache)

	with open(mod.config.path('stage/client/bb.class'), 'wb') as file:
		file.write(cf_assemble(cf))

	print('Patched client:bb.class → net.minecraft.client.render.ItemRenderer')

def _modify_render_item_decoration_method(cf, cp_cache):
	m = get_method(cf, cp_cache, 'b', '(Lsj;Lji;Liz;II)V')
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = a_code_load(a[0x02])

	a_code[0x01] = (13).to_bytes(2)
	a_code[0x03] = a_code[0x03][0:288] + assemble_code(cf, cp_cache, 0, 288, [
		['aload', 3],
		['ifnull', 'end'],

		['aload', 3],
		['invokevirtual', 'iz', 'a', '()Lgm;'],
		['getstatic', 'gm', 'BOTTLE', 'Lgm;'],
		['if_acmpne', 'end'],

		['aload', 3],
		['invokevirtual', 'iz', 'i', '()I'],
		['bipush', 100],
		['if_icmpge', 'end'],

		['aload', 3],
		['invokevirtual', 'iz', 'i', '()I'],
		'i2f',
		['sipush', 100],
		'i2f',
		'fdiv',
		['bipush', 13],
		'i2f',
		'fmul',
		['invokestatic', 'java/lang/Math', 'round', '(F)I'],
		['istore', 12],

		['sipush', 2896],
		['invokestatic', 'org/lwjgl/opengl/GL11', 'glDisable', '(I)V'],
		['sipush', 2929],
		['invokestatic', 'org/lwjgl/opengl/GL11', 'glDisable', '(I)V'],
		['sipush', 3553],
		['invokestatic', 'org/lwjgl/opengl/GL11', 'glDisable', '(I)V'],

		['getstatic', 'nw', 'a', 'Lnw;'],
		['astore', 8],

		['aload', 0],
		['aload', 8],
		['iload', 4], 'iconst_2', 'iadd',
		['iload', 5], ['bipush', 13], 'iadd',
		['bipush', 13],
		'iconst_2',
		'iconst_0',
		['invokevirtual', 'bb', 'a', '(Lnw;IIIII)V'],

		['aload', 0],
		['aload', 8],
		['iload', 4], 'iconst_2', 'iadd',
		['iload', 5], ['bipush', 13], 'iadd',
		['iload', 12],
		'iconst_1',
		['ldc_w.i32', struct.pack('>I', 0xff66cccc)],
		['invokevirtual', 'bb', 'a', '(Lnw;IIIII)V'],

		['sipush', 3553],
		['invokestatic', 'org/lwjgl/opengl/GL11', 'glEnable', '(I)V'],
		['sipush', 2896],
		['invokestatic', 'org/lwjgl/opengl/GL11', 'glEnable', '(I)V'],
		['sipush', 2929],
		['invokestatic', 'org/lwjgl/opengl/GL11', 'glEnable', '(I)V'],

		'fconst_1',
		'fconst_1',
		'fconst_1',
		'fconst_1',
		['invokestatic', 'org/lwjgl/opengl/GL11', 'glColor4f', '(FFFF)V'],

		['label', 'end'],
		'return'
	])
	a_code[0x02] = len(a_code[0x03]).to_bytes(4)

	for i, attribute in enumerate(a_code[0x07]):
		if get_utf8_at(cp_cache, int.from_bytes(attribute[0x00])).__eq__('LineNumberTable'):
			del a_code[0x07][i]
			break

	a_code[0x06] = len(a_code[0x07]).to_bytes(2)

	a[0x02] = a_code_assemble(a_code)
	a[0x01] = len(a[0x02]).to_bytes(4)
