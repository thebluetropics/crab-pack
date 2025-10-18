from modmaker import *
import mod, struct

def apply():
	if not mod.config.is_feature_enabled('fancy_tooltips'):
		return

	cf = load_class_file(mod.config.path('stage/client/id.class'))
	cp_cache = cp_init_cache(cf[0x04])

	modify_render_method(cf, cp_cache)

	with open(mod.config.path('stage/client/id.class'), 'wb') as file:
		file.write(cf_assemble(cf))

	print('Patched client:id.class → HandledScreen')

def modify_render_method(cf, cp_cache):
	m = get_method(cf, cp_cache, 'a', '(IIF)V')
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = a_code_load(a[0x02])

	a_code[0x03] = a_code[0x03][0:329] + assemble_code(cf, cp_cache, 0, 329, [
		['aload', 7],
		['invokevirtual', 'ix', 'i', '()Liz;'],
		['ifnonnull', 'skip'],

		['aload', 6],
		['ifnull', 'skip'],

		['aload', 6],
		['invokevirtual', 'gp', 'b', '()Z'],
		['ifeq', 'skip'],

		['new', 'java/lang/StringBuilder'],
		'dup',
		['invokespecial', 'java/lang/StringBuilder', '<init>', '()V'],
		['ldc_w.string', ''],
		['invokevirtual', 'java/lang/StringBuilder', 'append', '(Ljava/lang/String;)Ljava/lang/StringBuilder;'],
		['invokestatic', 'nh', 'a', '()Lnh;'],
		['aload', 6],
		['invokevirtual', 'gp', 'a', '()Liz;'],
		['invokevirtual', 'iz', 'l', '()Ljava/lang/String;'],
		['invokevirtual', 'nh', 'b', '(Ljava/lang/String;)Ljava/lang/String;'],
		['invokevirtual', 'java/lang/StringBuilder', 'append', '(Ljava/lang/String;)Ljava/lang/StringBuilder;'],
		['invokevirtual', 'java/lang/StringBuilder', 'toString', '()Ljava/lang/String;'],
		['invokevirtual', 'java/lang/String', 'trim', '()Ljava/lang/String;'],
		['astore', 8],

		['aload', 8],
		['invokevirtual', 'java/lang/String', 'length', '()I'],
		['ifle', 'skip'],

		'iload_1', ['iload', 4], 'isub', ['bipush', 12], 'iadd', ['istore', 9],
		'iload_2', ['iload', 5], 'isub', ['bipush', 12], 'isub', ['istore', 10],

		'aload_0',
		['getfield', 'id', 'g', 'Lsj;'],
		['aload', 8],
		['invokevirtual', 'sj', 'a', '(Ljava/lang/String;)I'],
		['istore', 11],

		'aload_0',
		['iload', 9],  'iconst_2', 'isub',
		['iload', 10], 'iconst_2', 'isub',
		['iload', 9], ['iload', 11], 'iadd', 'iconst_2', 'iadd',
		['iload', 10], ['bipush', 8], 'iadd', 'iconst_2', 'iadd',
		['ldc_w.i32', struct.pack('>I', 0xcc000000)],
		['invokevirtual', 'id', 'a', '(IIIII)V'],

		'aload_0',
		['iload', 9],  'iconst_3', 'isub',
		['iload', 10], 'iconst_3', 'isub',
		['iload', 9], ['iload', 11], 'iadd', 'iconst_3', 'iadd',
		['iload', 10], 'iconst_2', 'isub',
		['ldc_w.i32', struct.pack('>I', 0xff7f7f7f)],
		['invokevirtual', 'id', 'a', '(IIIII)V'],

		'aload_0',
		['iload', 9],  'iconst_3', 'isub',
		['iload', 10], ['bipush', 8], 'iadd', 'iconst_2', 'iadd',
		['iload', 9], ['iload', 11], 'iadd', 'iconst_3', 'iadd',
		['iload', 10], ['bipush', 8], 'iadd', 'iconst_3', 'iadd',
		['ldc_w.i32', struct.pack('>I', 0xff7f7f7f)],
		['invokevirtual', 'id', 'a', '(IIIII)V'],

		'aload_0',
		['iload', 9],  'iconst_3', 'isub',
		['iload', 10], 'iconst_2', 'isub',
		['iload', 9], 'iconst_2', 'isub',
		['iload', 10], ['bipush', 8], 'iadd', 'iconst_2', 'iadd',
		['ldc_w.i32', struct.pack('>I', 0xff7f7f7f)],
		['invokevirtual', 'id', 'a', '(IIIII)V'],

		'aload_0',
		['iload', 9],  ['iload', 11], 'iadd', 'iconst_2', 'iadd',
		['iload', 10], 'iconst_2', 'isub',
		['iload', 9], ['iload', 11], 'iadd', 'iconst_3', 'iadd',
		['iload', 10], ['bipush', 8], 'iadd', 'iconst_2', 'iadd',
		['ldc_w.i32', struct.pack('>I', 0xff7f7f7f)],
		['invokevirtual', 'id', 'a', '(IIIII)V'],

		'aload_0',
		['iload', 9],  'iconst_3', 'isub',
		['iload', 10], 'iconst_4', 'isub',
		['iload', 9], ['iload', 11], 'iadd', 'iconst_3', 'iadd',
		['iload', 10], 'iconst_3', 'isub',
		['ldc_w.i32', struct.pack('>I', 0xcc000000)],
		['invokevirtual', 'id', 'a', '(IIIII)V'],

		'aload_0',
		['iload', 9],  'iconst_3', 'isub',
		['iload', 10], ['bipush', 8], 'iadd', 'iconst_3', 'iadd',
		['iload', 9], ['iload', 11], 'iadd', 'iconst_3', 'iadd',
		['iload', 10], ['bipush', 8], 'iadd', 'iconst_4', 'iadd',
		['ldc_w.i32', struct.pack('>I', 0xcc000000)],
		['invokevirtual', 'id', 'a', '(IIIII)V'],

		'aload_0',
		['iload', 9],  'iconst_4', 'isub',
		['iload', 10], 'iconst_3', 'isub',
		['iload', 9], 'iconst_3', 'isub',
		['iload', 10], ['bipush', 8], 'iadd', 'iconst_3', 'iadd',
		['ldc_w.i32', struct.pack('>I', 0xcc000000)],
		['invokevirtual', 'id', 'a', '(IIIII)V'],

		'aload_0',
		['iload', 9],  ['iload', 11], 'iadd', 'iconst_3', 'iadd',
		['iload', 10], 'iconst_3', 'isub',
		['iload', 9], ['iload', 11], 'iadd', 'iconst_4', 'iadd',
		['iload', 10], ['bipush', 8], 'iadd', 'iconst_3', 'iadd',
		['ldc_w.i32', struct.pack('>I', 0xcc000000)],
		['invokevirtual', 'id', 'a', '(IIIII)V'],

		'aload_0',
		['getfield', 'id', 'g', 'Lsj;'],
		['aload', 8],
		['iload', 9],
		['iload', 10],
		'iconst_m1',
		['invokevirtual', 'sj', 'a', '(Ljava/lang/String;III)V'],

		['label', 'skip']
	]) + a_code[0x03][468:491]

	a_code[0x02] = len(a_code[0x03]).to_bytes(4)

	for i, attribute in enumerate(a_code[0x07]):
		if get_utf8_at(cp_cache, int.from_bytes(attribute[0x00])).__eq__('LineNumberTable'):
			del a_code[0x07][i]
			break

	a_code[0x06] = len(a_code[0x07]).to_bytes(2)

	a[0x02] = a_code_assemble(a_code)
	a[0x01] = len(a[0x02]).to_bytes(4)
