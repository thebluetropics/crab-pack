from modmaker import *
import os, mod

def apply(side_name):
	if not mod.config.is_feature_enabled('etc.hunger_and_thirst'):
		return

	side = 0 if side_name.__eq__('client') else 1
	c_name = 'com/thebluetropics/crabpack/BottleItem'

	cf = cf_create()
	cp_cache = cp_init_cache(cf[0x04])

	cf[0x02] = (49).to_bytes(2)

	cf[0x05] = (0x0001.__or__(0x0020)).to_bytes(2)
	cf[0x06] = i2cpx_c(cf, cp_cache, c_name)
	cf[0x07] = i2cpx_c(cf, cp_cache, ['gm', 'ej'][side])

	cf[0x0d].append(_create_constructor(cf, cp_cache, side, c_name))
	cf[0x0d].append(_create_use_method(cf, cp_cache, side_name, side))
	cf[0x0c] = len(cf[0x0d]).to_bytes(2)

	if not os.path.exists(f'stage/{side_name}/com/thebluetropics/crabpack'):
		os.makedirs(f'stage/{side_name}/com/thebluetropics/crabpack', exist_ok=True)

	with open(mod.config.path(f'stage/{side_name}/{c_name}.class'), 'wb') as file:
		file.write(cf_assemble(cf))

	print(f'Patched {side_name}:{c_name}.class')

def _create_constructor(cf, cp_cache, side, c_name):
	m = create_method(cf, cp_cache, ['public'], '<init>', '(I)V')

	code = assemble_code(cf, cp_cache, side, 0, [
		'aload_0',
		'iload_1',
		['invokespecial', ('gm', 'ej'), '<init>', '(I)V'],

		'aload_0',
		'iconst_1',
		['putfield', c_name, 'bg', 'I'],

		'return'
	])
	a_code = a_code_assemble([
		(2).to_bytes(2),
		(2).to_bytes(2),
		len(code).to_bytes(4),
		code,
		(0).to_bytes(2),
		[],
		(0).to_bytes(2),
		[]
	])

	m[0x03] = (1).to_bytes(2)
	m[0x04] = [[i2cpx_utf8(cf, cp_cache, 'Code'), len(a_code).to_bytes(4), a_code]]

	return m

def _get_instructions_for_use_method(cf, cp_cache, side_name, side):
	c_name_1 = ['bc', 'al'][side]
	cf_1 = load_class_file(mod.config.path(f'stage/{side_name}/{c_name_1}.class'))
	cp_cache_1 = cp_init_cache(cf_1[0x04])

	m = get_method(cf_1, cp_cache_1, 'a', ['(Liz;Lfd;Lgs;)Liz;', '(Lfy;Ldj;Lem;)Lfy;'][side])
	a = get_attribute(m[0x04], cp_cache_1, 'Code')

	a_code = a_code_load(a[0x02])
	code = load_code(cp_cache_1, a_code[0x03][0:243])
	code = code[0:130] + ['iconst_1'] + code[136:len(code)]
	final_code = assemble_code(cf, cp_cache, side, 0, code)

	return final_code

def _create_use_method(cf, cp_cache, side_name, side):
	included_instructions = _get_instructions_for_use_method(cf, cp_cache, side_name, side)
	m = create_method(cf, cp_cache, ['public'], 'a', ['(Liz;Lfd;Lgs;)Liz;', '(Lfy;Ldj;Lem;)Lfy;'][side])

	code = included_instructions + assemble_code(cf, cp_cache, side, len(included_instructions), [
		['aload', 24],
		['ifnull', 'do_not_refill'],

		['aload', 24],
		['getfield', ('vf', 'nh'), 'a', ('Ljg;', 'Lgd;')],
		['getstatic', ('jg', 'gd'), 'a', ('Ljg;', 'Lgd;')],
		['if_acmpne', 'do_not_refill'],

		['aload', 2],
		['aload', 24],
		['getfield', ('vf', 'nh'), 'b', 'I'],
		['aload', 24],
		['getfield', ('vf', 'nh'), 'c', 'I'],
		['aload', 24],
		['getfield', ('vf', 'nh'), 'd', 'I'],
		['invokevirtual', ('fd', 'dj'), ('f', 'd'), ('(III)Lln;', '(III)Lhj;')],
		['getstatic', ('ln', 'hj'), 'g', ('Lln;', 'Lhj;')],
		['if_acmpne', 'do_not_refill'],

		['aload', 1],
		['invokevirtual', ('iz', 'fy'), ('i', 'h'), '()I'],
		['bipush', 100],
		['if_icmpge', 'skip_inc'],

		['aload', 1],
		['aload', 1],
		['invokevirtual', ('iz', 'fy'), ('i', 'h'), '()I'],
		['bipush', 25],
		'iadd',
		['bipush', 100],
		['invokestatic', 'java/lang/Math', 'min', '(II)I'],
		['invokevirtual', ('iz', 'fy'), 'b', '(I)V'],

		['label', 'skip_inc'],
		['aload', 1],
		'areturn',

		['label', 'do_not_refill'],

		'aload_1',
		['invokevirtual', ('iz', 'fy'), ('i', 'h'), '()I'],
		['ifle', 'end'],

		'aload_1',
		['invokevirtual', ('iz', 'fy'), ('i', 'h'), '()I'],
		'iconst_5',
		['invokestatic', 'java/lang/Math', 'min', '(II)I'],
		['istore', 25],

		'aload_1',
		'aload_1',
		['invokevirtual', ('iz', 'fy'), ('i', 'h'), '()I'],
		['iload', 25],
		'isub',
		'iconst_0',
		['invokestatic', 'java/lang/Math', 'max', '(II)I'],
		['invokevirtual', ('iz', 'fy'), 'b', '(I)V'],

		'aload_3',
		['iload', 25],
		['invokevirtual', ('gs', 'em'), 'restoreThirst', '(I)V'],

		'aload_1',
		'areturn',

		['label', 'end'],

		'aload_1',
		'areturn'
	])
	a_code = a_code_assemble([
		(14).to_bytes(2),
		(26).to_bytes(2),
		len(code).to_bytes(4),
		code,
		(0).to_bytes(2),
		[],
		(0).to_bytes(2),
		[]
	])

	m[0x03] = (1).to_bytes(2)
	m[0x04] = [[i2cpx_utf8(cf, cp_cache, 'Code'), len(a_code).to_bytes(4), a_code]]

	return m
