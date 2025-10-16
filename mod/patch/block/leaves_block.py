from modmaker import *
import mod

def apply(side_name):
	if not mod.config.is_feature_enabled('block.persistent_leaves'):
		return

	side = 0 if side_name.__eq__('client') else 1
	c_name = ['bk', 'ar'][side]

	cf = load_class_file(mod.config.path(f'stage/{side_name}/{c_name}.class'))
	cp_cache = cp_init_cache(cf[0x04])

	_modify_after_break_method(cf, cp_cache, side, c_name)

	with open(mod.config.path(f'stage/{side_name}/{c_name}.class'), 'wb') as file:
		file.write(cf_assemble(cf))

	print(f'Patched {side_name}:{c_name}.class → net.minecraft.block.LeavesBlock')

def _modify_after_break_method(cf, cp_cache, side, c_name):
	m = get_method(cf, cp_cache, 'a', ['(Lfd;Lgs;IIII)V', '(Ldj;Lem;IIII)V'][side])
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = a_code_load(a[0x02])

	a_code[0x01] = (9).to_bytes(2)
	a_code[0x03] = assemble_code(cf, cp_cache, side, 0, [
		'aload_1', ['getfield', ('fd', 'dj'), 'B', 'Z'], ['ifne', 'L1'],

		'aload_2',
		['invokevirtual', ('gs', 'em'), 'G', ('()Liz;', '()Lfy;')],
		['ifnull', 'L1'],

		'aload_2',
		['invokevirtual', ('gs', 'em'), 'G', ('()Liz;', '()Lfy;')],
		['getfield', ('iz', 'fy'), 'c', 'I'],
		['getstatic', ('gm', 'ej'), 'bc', ('Lbl;', 'Las;')],
		['getfield', ('bl', 'as'), 'bf', 'I'],
		['if_icmpne', 'L1'],

		'aload_2',
		['getstatic', ('jl', 'gg'), 'C', ('[Lvr;', '[Lns;')],
		'aload_0',
		['getfield', c_name, 'bn', 'I'],
		'aaload',
		'iconst_1',
		['invokevirtual', ('gs', 'em'), 'a', ('(Lvr;I)V', '(Lns;I)V')],

		['iload', 6], 'iconst_3', 'iand', ['istore', 7],

		'iconst_0', ['istore', 8],

		['iload', 7], 'iconst_0', ['if_icmpne', 'birch'],
		'iconst_0', ['istore', 8],
		['goto', 'drop_item'],

		['label', 'birch'],
		['iload', 7], 'iconst_2', ['if_icmpne', 'spruce'],
		'iconst_1', ['istore', 8],
		['goto', 'drop_item'],

		['label', 'spruce'],
		['iload', 7], 'iconst_1', ['if_icmpne', 'drop_item'],
		'iconst_2', ['istore', 8],

		['label', 'drop_item'],

		'aload_0',
		'aload_1',
		'iload_3',
		['iload', 4],
		['iload', 5],
		['new', ('iz', 'fy')],
		'dup',
		['getstatic', ('uu', 'na'), 'PERSISTENT_LEAVES', 'Lcom/thebluetropics/crabpack/PersistentLeavesBlock;'],
		['getfield', 'com/thebluetropics/crabpack/PersistentLeavesBlock', 'bn', 'I'],
		'iconst_1',
		['iload', 8],
		['invokespecial', ('iz', 'fy'), '<init>', '(III)V'],
		['invokevirtual', c_name, 'a', ('(Lfd;IIILiz;)V', '(Ldj;IIILfy;)V')],
		['goto', 'L4'],

		['label', 'L1'],
		'aload_0',
		'aload_1',
		'aload_2',
		'iload_3',
		['iload', 4],
		['iload', 5],
		['iload', 6],
		['invokespecial', ('nr', 'in'), 'a', ('(Lfd;Lgs;IIII)V', '(Ldj;Lem;IIII)V')],

		['label', 'L4'],
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
