from modmaker import *
import mod

def apply(side_name):
	if not mod.config.is_feature_enabled('block.mortar'):
		return

	side = 0 if side_name.__eq__('client') else 1
	c_name = ['rk', 'kr'][side]

	cf = load_class_file(mod.config.path(f'stage/{side_name}/{c_name}.class'))
	cp_cache = cp_init_cache(cf[0x04])

	_modify_use_on_block_method(cf, cp_cache, side)

	with open(mod.config.path(f'stage/{side_name}/{c_name}.class'), 'wb') as file:
		file.write(cf_assemble(cf))

	print(f'Patched {side_name}:{c_name}.class → net.minecraft.item.SeedsItem')

def _modify_use_on_block_method(cf, cp_cache, side):
	m = get_method(cf, cp_cache, 'a', ['(Liz;Lgs;Lfd;IIII)Z', '(Lfy;Lem;Ldj;IIII)Z'][side])
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = a_code_load(a[0x02])

	a_code[0x03] = assemble_code(cf, cp_cache, side, 0, [
		'aload_3',
		['iload', 4],
		['iload', 5],
		['iload', 6],
		['invokevirtual', ('fd', 'dj'), 'a', '(III)I'],
		['sipush', 100],
		['if_icmpne', 'L3'],

		'aload_3',
		['getfield', ('fd', 'dj'), 'B', 'Z'],
		['ifne', 'L3'],

		'aload_3',
		['iload', 4],
		['iload', 5],
		['iload', 6],
		['invokevirtual', ('fd', 'dj'), ('e', 'c'), '(III)I'],
		'iconst_0',
		['if_icmpne', 'L1'],

		'aload_3',
		['iload', 4],
		['iload', 5],
		['iload', 6],
		'iconst_1',
		['invokevirtual', ('fd', 'dj'), ('d', 'c'), '(IIII)V'],

		'aload_1',
		'dup',
		['getfield', ('iz', 'fy'), 'a', 'I'],
		'iconst_1',
		'isub',
		['putfield', ('iz', 'fy'), 'a', 'I'],

		'iconst_1',
		'ireturn',

		['label', 'L1'],
		'aload_3',
		['iload', 4],
		['iload', 5],
		['iload', 6],
		['invokevirtual', ('fd', 'dj'), ('e', 'c'), '(III)I'],
		'iconst_1',
		['if_icmpne', 'L2'],

		'aload_3',
		['iload', 4],
		['iload', 5],
		['iload', 6],
		'iconst_2',
		['invokevirtual', ('fd', 'dj'), ('d', 'c'), '(IIII)V'],

		'aload_1',
		'dup',
		['getfield', ('iz', 'fy'), 'a', 'I'],
		'iconst_1',
		'isub',
		['putfield', ('iz', 'fy'), 'a', 'I'],

		'iconst_1',
		'ireturn',

		['label', 'L2'],
		'aload_3',
		['iload', 4],
		['iload', 5],
		['iload', 6],
		['invokevirtual', ('fd', 'dj'), ('e', 'c'), '(III)I'],
		'iconst_2',
		['if_icmpne', 'L3'],

		'aload_3',
		['iload', 4],
		['iload', 5],
		['iload', 6],
		'iconst_3',
		['invokevirtual', ('fd', 'dj'), ('d', 'c'), '(IIII)V'],

		'aload_1',
		'dup',
		['getfield', ('iz', 'fy'), 'a', 'I'],
		'iconst_1',
		'isub',
		['putfield', ('iz', 'fy'), 'a', 'I'],

		'iconst_1',
		'ireturn',

		['label', 'L3']
	]) + a_code[0x03][0:77]
	a_code[0x02] = len(a_code[0x03]).to_bytes(4)

	# remove line number table
	a_code[0x06] = (int.from_bytes(a_code[0x06]) - 1).to_bytes(2)

	for i, a in a_code[0x07]:
		if get_utf8_at(cp_cache, int.from_bytes(a[0x00])).__eq__('LineNumberTable'):
			del a_code[0x07][i]
			break

	# update code attribute
	a[0x02] = a_code_assemble(a_code)

	# update code attribute length
	a[0x01] = len(a[0x02]).to_bytes(4)
