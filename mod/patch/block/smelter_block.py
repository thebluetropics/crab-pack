from modmaker import *
import os, mod

def apply(side_name):
	if not mod.config.is_feature_enabled('block.smelter'):
		return

	side = 0 if side_name.__eq__('client') else 1
	c_name = 'com/thebluetropics/crabpack/SmelterBlock'

	cf = cf_create()
	cp_cache = cp_init_cache(cf[0x04])

	cf[0x02] = (49).to_bytes(2)

	cf[0x05] = (0x0001.__or__(0x0020)).to_bytes(2)
	cf[0x06] = i2cpx_c(cf, cp_cache, c_name)
	cf[0x07] = i2cpx_c(cf, cp_cache, ['rw', 'lb'][side])

	cf[0x0b].append(create_field(cf, cp_cache, ['private'], 'random', 'Ljava/util/Random;'))
	cf[0x0a] = len(cf[0x0b]).to_bytes(2)

	cf[0x0d].append(_create_constructor(cf, cp_cache, side, c_name))
	cf[0x0d].append(_create_on_placed_method(cf, cp_cache, side))
	cf[0x0d].append(_create_create_block_entity_method(cf, cp_cache, side))
	cf[0x0d].append(_create_on_use_method(cf, cp_cache, side))
	cf[0x0d].append(_create_update_lit_state_method(cf, cp_cache, side))
	cf[0x0d].append(_create_on_break_method(cf, cp_cache, side, c_name))

	if side_name.__eq__('client'):
		cf[0x0d].append(_create_get_texture_id_method(cf, cp_cache))
		cf[0x0d].append(_create_get_texture_method(cf, cp_cache))

	cf[0x0c] = len(cf[0x0d]).to_bytes(2)

	if not os.path.exists(f'stage/{side_name}/com/thebluetropics/crabpack'):
		os.makedirs(f'stage/{side_name}/com/thebluetropics/crabpack', exist_ok=True)

	with open(mod.config.path(f'stage/{side_name}/{c_name}.class'), 'wb') as file:
		file.write(cf_assemble(cf))

	print(f'Created {side_name}:SmelterBlock.class')

def _create_constructor(cf, cp_cache, side, c_name):
	m = create_method(cf, cp_cache, ['public'], '<init>', '(I)V')

	code = assemble_code(cf, cp_cache, side, 0, [
		'aload_0',
		'iload_1',
		['getstatic', ('ln', 'hj'), 'b', ('Lln;', 'Lhj;')],
		['invokespecial', ('rw', 'lb'), '<init>', ('(ILln;)V', '(ILhj;)V')],
		'aload_0',
		['sipush', 226],
		['putfield', c_name, 'bm', 'I'],
		'aload_0',
		['new', 'java/util/Random'],
		'dup',
		['invokespecial', 'java/util/Random', '<init>', '()V'],
		['putfield', c_name, 'random', 'Ljava/util/Random;'],
		'return'
	])
	a_code = a_code_assemble([
		(3).to_bytes(2),
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

def _create_on_placed_method(cf, cp_cache, side):
	m = create_method(cf, cp_cache, ['public'], 'a', ['(Lfd;IIILls;)V', '(Ldj;IIILhl;)V'][side])

	code = assemble_code(cf, cp_cache, side, 0, [
		['aload', 5],
		['getfield', ('ls', 'hl'), ('aS', 'aV'), 'F'],
		['ldc.f32', 4.0],
		'fmul',
		['ldc.f32', 360.0],
		'fdiv',
		'f2d',
		['ldc2_w.f64', 0.5],
		'dadd',
		['invokestatic', ('in', 'fq'), 'b', '(D)I'],
		'iconst_3',
		'iand',
		['istore', 6],

		['iload', 6],
		'iconst_0',
		['if_icmpne', 'L1'],

		'aload_1',
		'iload_2', 'iload_3', ['iload', 4], 'iconst_0',
		['invokevirtual', ('fd', 'dj'), ('d', 'c'), '(IIII)V'],
		'return',

		['label', 'L1'],
		['iload', 6],
		'iconst_1',
		['if_icmpne', 'L2'],

		'aload_1',
		'iload_2',
		'iload_3',
		['iload', 4],
		'iconst_1',
		['invokevirtual', ('fd', 'dj'), ('d', 'c'), '(IIII)V'],
		'return',

		['label', 'L2'],
		['iload', 6],
		'iconst_2',
		['if_icmpne', 'L3'],

		'aload_1',
		'iload_2',
		'iload_3',
		['iload', 4],
		'iconst_2',
		['invokevirtual', ('fd', 'dj'), ('d', 'c'), '(IIII)V'],
		'return',

		['label', 'L3'],
		['iload', 6],
		'iconst_3',
		['if_icmpne', 'L4'],

		'aload_1',
		'iload_2',
		'iload_3',
		['iload', 4],
		'iconst_3',
		['invokevirtual', ('fd', 'dj'), ('d', 'c'), '(IIII)V'],
		'return',

		['label', 'L4'],

		'return'
	])
	a_code = a_code_assemble([
		(5).to_bytes(2),
		(7).to_bytes(2),
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

def _create_get_texture_id_method(cf, cp_cache):
	m = create_method(cf, cp_cache, ['public'], 'a', '(Lxp;IIII)I')

	code = assemble_code(cf, cp_cache, 0, 0, [
		'aload_1', 'iload_2', 'iload_3', ['iload', 4], ['invokeinterface', 'xp', 'e', '(III)I', 4],
		'iconst_3', 'iand',
		['istore', 6],

		'aload_1', 'iload_2', 'iload_3', ['iload', 4], ['invokeinterface', 'xp', 'e', '(III)I', 4],
		'iconst_4', 'iand',
		'iconst_2', 'iushr',
		['istore', 7],

		['iload', 5], 'iconst_2', ['if_icmpne', 'Lskip_1'],
		['iload', 6], 'iconst_0', ['if_icmpne', 'Lret_229'],
		['iload', 7], ['ifeq', 'Lret_227'],
		['goto', 'Lret_228'],
		'ireturn',

		['label', 'Lskip_1'],
		['iload', 5], 'iconst_3', ['if_icmpne', 'Lskip_2'],
		['iload', 6], 'iconst_2', ['if_icmpne', 'Lret_229'],
		['iload', 7], ['ifeq', 'Lret_227'],
		['goto', 'Lret_228'],
		'ireturn',

		['label', 'Lskip_2'],
		['iload', 5], 'iconst_5', ['if_icmpne', 'Lskip_3'],
		['iload', 6], 'iconst_1', ['if_icmpne', 'Lret_229'],
		['iload', 7], ['ifeq', 'Lret_227'],
		['goto', 'Lret_228'],
		'ireturn',

		['label', 'Lskip_3'],
		['iload', 5], 'iconst_4', ['if_icmpne', 'Lskip_4'],
		['iload', 6], 'iconst_3', ['if_icmpne', 'Lret_229'],
		['iload', 7], ['ifeq', 'Lret_227'],
		['goto', 'Lret_228'],
		'ireturn',

		['label', 'Lskip_4'],
		['sipush', 226], 'ireturn',

		['label', 'Lret_227'], ['sipush', 227], 'ireturn',
		['label', 'Lret_228'], ['sipush', 228], 'ireturn',
		['label', 'Lret_229'], ['sipush', 229], 'ireturn'
	])
	a_code = a_code_assemble([
		(4).to_bytes(2),
		(8).to_bytes(2),
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

def _create_create_block_entity_method(cf, cp_cache, side):
	m = create_method(cf, cp_cache, ['protected'], 'a_', ['()Low;', '()Ljh;'][side])

	code = assemble_code(cf, cp_cache, side, 0, [
		['new', 'com/thebluetropics/crabpack/SmelterBlockEntity'],
		'dup',
		['invokespecial', 'com/thebluetropics/crabpack/SmelterBlockEntity', '<init>', '()V'],
		'areturn'
	])
	a_code = a_code_assemble([
		(2).to_bytes(2),
		(1).to_bytes(2),
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

def _create_on_use_method(cf, cp_cache, side):
	m = create_method(cf, cp_cache, ['public'], 'a', ['(Lfd;IIILgs;)Z', '(Ldj;IIILem;)Z'][side])

	code = assemble_code(cf, cp_cache, side, 0, [
		'aload_1',
		['getfield', ('fd', 'dj'), 'B', 'Z'],
		['ifeq', 'L1'],

		'iconst_1',
		'ireturn',

		['label', 'L1'],
		'aload_1',
		'iload_2',
		'iload_3',
		['iload', 4],
		['invokevirtual', ('fd', 'dj'), 'b', ('(III)Low;', '(III)Ljh;')],
		['checkcast', 'com/thebluetropics/crabpack/SmelterBlockEntity'],
		['astore', 6],

		['aload', 5],
		['aload', 6],
		['invokevirtual', ('gs', 'em'), 'openSmelterScreen', '(Lcom/thebluetropics/crabpack/SmelterBlockEntity;)V'],

		'iconst_1',
		'ireturn'
	])
	a_code = a_code_assemble([
		(4).to_bytes(2),
		(7).to_bytes(2),
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

def _create_update_lit_state_method(cf, cp_cache, side):
	m = create_method(cf, cp_cache, ['public', 'static'], 'updateLitState', ['(ZLfd;III)V', '(ZLdj;III)V'][side])

	code = assemble_code(cf, cp_cache, side, 0, [
		'aload_1',
		'iload_2',
		'iload_3',
		['iload', 4],
		['invokevirtual', ('fd', 'dj'), ('e', 'c'), '(III)I'],
		['istore', 5],

		'iload_0',
		['ifeq', 'L0'],

		'aload_1',
		'iload_2',
		'iload_3',
		['iload', 4],
		['iload', 5],
		['bipush', 7],
		'iand',
		['invokevirtual', ('fd', 'dj'), ('d', 'c'), '(IIII)V'],

		['label', 'L0'],
		'iload_0',
		['ifne', 'L1'],

		'aload_1',
		'iload_2',
		'iload_3',
		['iload', 4],
		['iload', 5],
		'iconst_3',
		'iand',
		['invokevirtual', ('fd', 'dj'), ('d', 'c'), '(IIII)V'],

		['label', 'L1'],
		'return'
	])
	a_code = a_code_assemble([
		(6).to_bytes(2),
		(6).to_bytes(2),
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

def _create_get_texture_method(cf, cp_cache):
	m = create_method(cf, cp_cache, ['public'], 'a', '(I)I')

	code = assemble_code(cf, cp_cache, 0, 0, [
		'iload_1',
		'iconst_1',
		['if_icmpeq', 'L226'],

		'iload_1',
		'iconst_2',
		['if_icmpeq', 'L226'],

		'iload_1',
		'iconst_3',
		['if_icmpeq', 'L227'],

		['sipush', 229],
		'ireturn',

		['label', 'L227'],
		['sipush', 227],
		'ireturn',

		['label', 'L226'],
		['sipush', 226],
		'ireturn'
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

def _create_on_break_method(cf, cp_cache, side, c_name):
	m = create_method(cf, cp_cache, ['public'], 'b', ['(Lfd;III)V', '(Ldj;III)V'][side])

	code = assemble_code(cf, cp_cache, side, 0, [
		'aload_1',
		'iload_2',
		'iload_3',
		['iload', 4],
		['invokevirtual', ('fd', 'dj'), 'b', ('(III)Low;', '(III)Ljh;')],
		['checkcast', 'com/thebluetropics/crabpack/SmelterBlockEntity'],
		['astore', 5],

		'iconst_0',
		['istore', 6],

		['label', 'L4'],
		['iload', 6],
		['aload', 5],
		['invokeinterface', ('lw', 'hp'), 'a', '()I', 1],
		['if_icmpge', 'L1'],

		['label', 'L5'],
		['aload', 5],
		['iload', 6],
		['invokeinterface', ('lw', 'hp'), ('f_', 'd_'), ('(I)Liz;', '(I)Lfy;'), 2],
		['astore', 7],

		['label', 'L6'],
		['aload', 7],
		['ifnull', 'L7'],

		['label', 'L8'],
		'aload_0',
		['getfield', c_name, 'random', 'Ljava/util/Random;'],
		['invokevirtual', 'java/util/Random', 'nextFloat', '()F'],
		['ldc.f32', 0.8],
		'fmul',
		['ldc.f32', 0.1],
		'fadd',
		['fstore', 8],

		'aload_0',
		['getfield', c_name, 'random', 'Ljava/util/Random;'],
		['invokevirtual', 'java/util/Random', 'nextFloat', '()F'],
		['ldc.f32', 0.8],
		'fmul',
		['ldc.f32', 0.1],
		'fadd',
		['fstore', 9],

		'aload_0',
		['getfield', c_name, 'random', 'Ljava/util/Random;'],
		['invokevirtual', 'java/util/Random', 'nextFloat', '()F'],
		['ldc.f32', 0.8],
		'fmul',
		['ldc.f32', 0.1],
		'fadd',
		['fstore', 10],

		['label', 'L11'],
		['aload', 7],
		['getfield', ('iz', 'fy'), 'a', 'I'],
		['ifle', 'L7'],

		'aload_0',
		['getfield', c_name, 'random', 'Ljava/util/Random;'],
		['bipush', 21],
		['invokevirtual', 'java/util/Random', 'nextInt', '(I)I'],
		['bipush', 10],
		'iadd',
		['istore', 11],

		['iload', 11],
		['aload', 7],
		['getfield', ('iz', 'fy'), 'a', 'I'],
		['if_icmple', 'L14'],

		['aload', 7],
		['getfield', ('iz', 'fy'), 'a', 'I'],
		['istore', 11],

		['label', 'L14'],
		['aload', 7],
		'dup',
		['getfield', ('iz', 'fy'), 'a', 'I'],
		['iload', 11],
		'isub',
		['putfield', ('iz', 'fy'), 'a', 'I'],

		['new', ('hl', 'ez')],
		'dup',
		'aload_1',
		'iload_2',
		'i2f',
		['fload', 8],
		'fadd',
		'f2d',
		'iload_3',
		'i2f',
		['fload', 9],
		'fadd',
		'f2d',
		['iload', 4],
		'i2f',
		['fload', 10],
		'fadd',
		'f2d',
		['new', ('iz', 'fy')],
		'dup',
		['aload', 7],
		['getfield', ('iz', 'fy'), 'c', 'I'],
		['iload', 11],
		['aload', 7],
		['invokevirtual', ('iz', 'fy'), ('i', 'h'), '()I'],
		['invokespecial', ('iz', 'fy'), '<init>', '(III)V'],
		['invokespecial', ('hl', 'ez'), '<init>', ('(Lfd;DDDLiz;)V', '(Ldj;DDDLfy;)V')],
		['astore', 12],

		['ldc.f32', 0.05],
		['fstore', 13],

		['aload', 12],
		'aload_0',
		['getfield', c_name, 'random', 'Ljava/util/Random;'],
		['invokevirtual', 'java/util/Random', 'nextGaussian', '()D'],
		'd2f',
		['fload', 13],
		'fmul',
		'f2d',
		['putfield', ('hl', 'ez'), ('aP', 'aS'), 'D'],

		['aload', 12],
		'aload_0',
		['getfield', c_name, 'random', 'Ljava/util/Random;'],
		['invokevirtual', 'java/util/Random', 'nextGaussian', '()D'],
		'd2f',
		['fload', 13],
		'fmul',
		['ldc.f32', 0.2],
		'fadd',
		'f2d',
		['putfield', ('hl', 'ez'), ('aQ', 'aT'), 'D'],

		['aload', 12],
		'aload_0',
		['getfield', c_name, 'random', 'Ljava/util/Random;'],
		['invokevirtual', 'java/util/Random', 'nextGaussian', '()D'],
		'd2f',
		['fload', 13],
		'fmul',
		'f2d',
		['putfield', ('hl', 'ez'), ('aR', 'aU'), 'D'],

		'aload_1',
		['aload', 12],
		['invokevirtual', ('fd', 'dj'), 'b', ('(Lsn;)Z', '(Llq;)Z')],
		'pop',

		['goto', 'L11'],

		['label', 'L7'],
		['iinc', 6, 1],
		['goto', 'L4'],

		['label', 'L1'],
		'aload_0',
		'aload_1',
		'iload_2',
		'iload_3',
		['iload', 4],
		['invokespecial', ('rw', 'lb'), 'b', ('(Lfd;III)V', '(Ldj;III)V')],

		'return'
	])
	a_code = a_code_assemble([
		(14).to_bytes(2),
		(14).to_bytes(2),
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
