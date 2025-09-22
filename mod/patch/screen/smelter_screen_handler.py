import os, mod

from modmaker.a_code import (
	a_code_assemble,
	assemble_code
)
from modmaker.cf import (
	cf_assemble,
	cf_create
)
from modmaker.cp import (
	cp_init_cache,
	i2cpx_utf8,
	i2cpx_c
)
from modmaker.f import (
	create_field
)
from modmaker.m import (
	create_method
)

def apply(side_name):
	side = 0 if side_name.__eq__('client') else 1
	c_name = 'com/thebluetropics/crabpack/SmelterScreenHandler'

	cf = cf_create()
	cp_cache = cp_init_cache(cf[0x04])

	cf[0x02] = (49).to_bytes(2)

	cf[0x05] = (0x0001.__or__(0x0020)).to_bytes(2)
	cf[0x06] = i2cpx_c(cf, cp_cache, c_name)
	cf[0x07] = i2cpx_c(cf, cp_cache, ['dw', 'cl'][side])

	cf[0x0b].append(create_field(cf, cp_cache, ['private'], 'blockEntity', 'Lcom/thebluetropics/crabpack/SmelterBlockEntity;'))
	cf[0x0b].append(create_field(cf, cp_cache, ['private'], 'cookTime', 'I'))
	cf[0x0b].append(create_field(cf, cp_cache, ['private'], 'burnTime', 'I'))
	cf[0x0b].append(create_field(cf, cp_cache, ['private'], 'fuelTime', 'I'))
	cf[0x0a] = len(cf[0x0b]).to_bytes(2)

	cf[0x0d].append(_create_constructor(cf, cp_cache, side, c_name))
	cf[0x0d].append(_create_send_content_updates_method(cf, cp_cache, side, c_name))
	cf[0x0d].append(_create_can_use_method(cf, cp_cache, side, c_name))

	if side_name.__eq__('client'):
		cf[0x0d].append(_create_set_property_method(cf, cp_cache, c_name))

	if side_name.__eq__('server'):
		cf[0x0d].append(_create_add_listener_method(cf, cp_cache, c_name))

	cf[0x0c] = len(cf[0x0d]).to_bytes(2)

	if not os.path.exists(f'stage/{side_name}/com/thebluetropics/crabpack'):
		os.makedirs(f'stage/{side_name}/com/thebluetropics/crabpack', exist_ok=True)

	with open(mod.config.path(f'stage/{side_name}/{c_name}.class'), 'wb') as file:
		file.write(cf_assemble(cf))

	print(f'Created {side_name}:SmelterScreenHandler.class')

def _create_constructor(cf, cp_cache, side, c_name):
	m = create_method(cf, cp_cache, ['public'], '<init>', ['(Lix;Lcom/thebluetropics/crabpack/SmelterBlockEntity;)V', '(Lfx;Lcom/thebluetropics/crabpack/SmelterBlockEntity;)V'][side])

	code = assemble_code(cf, cp_cache, side, 0, [
		'aload_0',
		['invokespecial', ('dw', 'cl'), '<init>', '()V'],

		'aload_0',
		'iconst_0',
		['putfield', c_name, 'cookTime', 'I'],

		'aload_0',
		'iconst_0',
		['putfield', c_name, 'burnTime', 'I'],

		'aload_0',
		'iconst_0',
		['putfield', c_name, 'fuelTime', 'I'],

		'aload_0',
		['aload', 2],
		['putfield', c_name, 'blockEntity', 'Lcom/thebluetropics/crabpack/SmelterBlockEntity;'],

		'aload_0',
		['new', ('gp', 'el')],
		'dup',
		['aload', 2],
		'iconst_0',
		['bipush', 42],
		['bipush', 12],
		['invokespecial', ('gp', 'el'), '<init>', ('(Llw;III)V', '(Lhp;III)V')],
		['invokevirtual', c_name, 'a', ('(Lgp;)V', '(Lel;)V')],

		'aload_0',
		['new', ('gp', 'el')],
		'dup',
		['aload', 2],
		'iconst_1',
		['bipush', 60],
		['bipush', 12],
		['invokespecial', ('gp', 'el'), '<init>', ('(Llw;III)V', '(Lhp;III)V')],
		['invokevirtual', c_name, 'a', ('(Lgp;)V', '(Lel;)V')],

		'aload_0',
		['new', ('gp', 'el')],
		'dup',
		['aload', 2],
		'iconst_2',
		['bipush', 51],
		['bipush', 48],
		['invokespecial', ('gp', 'el'), '<init>', ('(Llw;III)V', '(Lhp;III)V')],
		['invokevirtual', c_name, 'a', ('(Lgp;)V', '(Lel;)V')],

		'aload_0',
		['new', 'com/thebluetropics/crabpack/SmelterOutputSlot'],
		'dup',
		['aload', 1],
		['getfield', ('ix', 'fx'), 'd', ('Lgs;', 'Lem;')],
		['aload', 2],
		'iconst_3',
		['bipush', 114],
		['bipush', 30],
		['invokespecial', 'com/thebluetropics/crabpack/SmelterOutputSlot', '<init>', ('(Lgs;Llw;III)V', '(Lem;Lhp;III)V')],
		['invokevirtual', c_name, 'a', ('(Lgp;)V', '(Lel;)V')],

		'iconst_0',
		['istore', 3],

		['label', 'L9'],
		['iload', 3],
		'iconst_3',
		['if_icmpge', 'L10'],

		'iconst_0',
		['istore', 4],

		['label', 'L12'],
		['iload', 4],
		['bipush', 9],
		['if_icmpge', 'L13'],

		'aload_0',
		['new', ('gp', 'el')],
		'dup',
		['aload', 1],
		['iload', 4],
		['iload', 3],
		['bipush', 9],
		'imul',
		'iadd',
		['bipush', 9],
		'iadd',
		['bipush', 8],
		['iload', 4],
		['bipush', 18],
		'imul',
		'iadd',
		['bipush', 74],
		['iload', 3],
		['bipush', 18],
		'imul',
		'iadd',
		['invokespecial', ('gp', 'el'), '<init>', ('(Llw;III)V', '(Lhp;III)V')],
		['invokevirtual', c_name, 'a', ('(Lgp;)V', '(Lel;)V')],

		['iinc', 4, 1],
		['goto', 'L12'],

		['label', 'L13'],
		['iinc', 3, 1],
		['goto', 'L9'],

		['label', 'L10'],
		'iconst_0',
		['istore', 3],

		['label', 'L16'],
		['iload', 3],
		['bipush', 9],
		['if_icmpge', 'L17'],

		'aload_0',
		['new', ('gp', 'el')],
		'dup',
		['aload', 1],
		['iload', 3],
		['bipush', 8],
		['iload', 3],
		['bipush', 18],
		'imul',
		'iadd',
		['sipush', 132],
		['invokespecial', ('gp', 'el'), '<init>', ('(Llw;III)V', '(Lhp;III)V')],
		['invokevirtual', c_name, 'a', ('(Lgp;)V', '(Lel;)V')],

		['iinc', 3, 1],
		['goto', 'L16'],

		['label', 'L17'],
		'return'
	])
	a_code = a_code_assemble([
		(9).to_bytes(2),
		(5).to_bytes(2),
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

def _create_send_content_updates_method(cf, cp_cache, side, c_name):
	m = create_method(cf, cp_cache, ['public'], 'a', '()V')

	code = assemble_code(cf, cp_cache, side, 0, [
		'aload_0',
		['invokespecial', ('dw', 'cl'), 'a', '()V'],
		'iconst_0',
		'istore_1',
		['label', 'L2'],
		'iload_1',
		'aload_0',
		['getfield', c_name, 'g', 'Ljava/util/List;'],
		['invokeinterface', 'java/util/List', 'size', '()I', 1],
		['if_icmpge', 'L3'],
		'aload_0',
		['getfield', c_name, 'g', 'Ljava/util/List;'],
		'iload_1',
		['invokeinterface', 'java/util/List', 'get', '(I)Ljava/lang/Object;', 2],
		['checkcast', ('ec', 'cp')],
		['astore', 2],
		'aload_0',
		['getfield', c_name, 'cookTime', 'I'],
		'aload_0',
		['getfield', c_name, 'blockEntity', 'Lcom/thebluetropics/crabpack/SmelterBlockEntity;'],
		['getfield', 'com/thebluetropics/crabpack/SmelterBlockEntity', 'cookTime', 'I'],
		['if_icmpeq', 'L6'],
		['aload', 2],
		'aload_0',
		'iconst_0',
		'aload_0',
		['getfield', c_name, 'blockEntity', 'Lcom/thebluetropics/crabpack/SmelterBlockEntity;'],
		['getfield', 'com/thebluetropics/crabpack/SmelterBlockEntity', 'cookTime', 'I'],
		['invokeinterface', ('ec', 'cp'), 'a', ('(Ldw;II)V', '(Lcl;II)V'), 4],
		['label', 'L6'],
		'aload_0',
		['getfield', c_name, 'burnTime', 'I'],
		'aload_0',
		['getfield', c_name, 'blockEntity', 'Lcom/thebluetropics/crabpack/SmelterBlockEntity;'],
		['getfield', 'com/thebluetropics/crabpack/SmelterBlockEntity', 'burnTime', 'I'],
		['if_icmpeq', 'L8'],
		['aload', 2],
		'aload_0',
		'iconst_1',
		'aload_0',
		['getfield', c_name, 'blockEntity', 'Lcom/thebluetropics/crabpack/SmelterBlockEntity;'],
		['getfield', 'com/thebluetropics/crabpack/SmelterBlockEntity', 'burnTime', 'I'],
		['invokeinterface', ('ec', 'cp'), 'a', ('(Ldw;II)V', '(Lcl;II)V'), 4],
		['label', 'L8'],
		'aload_0',
		['getfield', c_name, 'fuelTime', 'I'],
		'aload_0',
		['getfield', c_name, 'blockEntity', 'Lcom/thebluetropics/crabpack/SmelterBlockEntity;'],
		['getfield', 'com/thebluetropics/crabpack/SmelterBlockEntity', 'fuelTime', 'I'],
		['if_icmpeq', 'L10'],
		['aload', 2],
		'aload_0',
		'iconst_2',
		'aload_0',
		['getfield', c_name, 'blockEntity', 'Lcom/thebluetropics/crabpack/SmelterBlockEntity;'],
		['getfield', 'com/thebluetropics/crabpack/SmelterBlockEntity', 'fuelTime', 'I'],
		['invokeinterface', ('ec', 'cp'), 'a', ('(Ldw;II)V', '(Lcl;II)V'), 4],
		['label', 'L10'],
		['iinc', 1, 1],
		['goto', 'L2'],
		['label', 'L3'],
		'aload_0',
		'aload_0',
		['getfield', c_name, 'blockEntity', 'Lcom/thebluetropics/crabpack/SmelterBlockEntity;'],
		['getfield', 'com/thebluetropics/crabpack/SmelterBlockEntity', 'cookTime', 'I'],
		['putfield', c_name, 'cookTime', 'I'],
		'aload_0',
		'aload_0',
		['getfield', c_name, 'blockEntity', 'Lcom/thebluetropics/crabpack/SmelterBlockEntity;'],
		['getfield', 'com/thebluetropics/crabpack/SmelterBlockEntity', 'burnTime', 'I'],
		['putfield', c_name, 'burnTime', 'I'],
		'aload_0',
		'aload_0',
		['getfield', c_name, 'blockEntity', 'Lcom/thebluetropics/crabpack/SmelterBlockEntity;'],
		['getfield', 'com/thebluetropics/crabpack/SmelterBlockEntity', 'fuelTime', 'I'],
		['putfield', c_name, 'fuelTime', 'I'],
		'return'
	])
	a_code = a_code_assemble([
		(4).to_bytes(2),
		(3).to_bytes(2),
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

def _create_set_property_method(cf, cp_cache, c_name):
	m = create_method(cf, cp_cache, ['public'], 'a', '(II)V')

	code = assemble_code(cf, cp_cache, 0, 0, [
		'iload_1',
		['ifne', 'L1'],
		'aload_0',
		['getfield', c_name, 'blockEntity', 'Lcom/thebluetropics/crabpack/SmelterBlockEntity;'],
		'iload_2',
		['putfield', 'com/thebluetropics/crabpack/SmelterBlockEntity', 'cookTime', 'I'],

		['label', 'L1'],
		'iload_1',
		'iconst_1',
		['if_icmpne', 'L2'],
		'aload_0',
		['getfield', c_name, 'blockEntity', 'Lcom/thebluetropics/crabpack/SmelterBlockEntity;'],
		'iload_2',
		['putfield', 'com/thebluetropics/crabpack/SmelterBlockEntity', 'burnTime', 'I'],

		['label', 'L2'],
		'iload_1',
		'iconst_2',
		['if_icmpne', 'L3'],
		'aload_0',
		['getfield', c_name, 'blockEntity', 'Lcom/thebluetropics/crabpack/SmelterBlockEntity;'],
		'iload_2',
		['putfield', 'com/thebluetropics/crabpack/SmelterBlockEntity', 'fuelTime', 'I'],

		['label', 'L3'],
		'return'
	])
	a_code = a_code_assemble([
		(2).to_bytes(2),
		(3).to_bytes(2),
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

def _create_can_use_method(cf, cp_cache, side, c_name):
	m = create_method(cf, cp_cache, ['public'], 'b', ['(Lgs;)Z', '(Lem;)Z'][side])

	code = assemble_code(cf, cp_cache, side, 0, [
		'aload_0',
		['getfield', c_name, 'blockEntity', 'Lcom/thebluetropics/crabpack/SmelterBlockEntity;'],
		'aload_1',
		['invokevirtual', 'com/thebluetropics/crabpack/SmelterBlockEntity', 'a_', ('(Lgs;)Z', '(Lem;)Z')],
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

def _create_add_listener_method(cf, cp_cache, c_name):
	m = create_method(cf, cp_cache, ['public'], 'a', '(Lcp;)V')

	code = assemble_code(cf, cp_cache, 1, 0, [
		'aload_0',
		'aload_1',
		['invokespecial', 'cl', 'a', '(Lcp;)V'],

		'aload_1',
		'aload_0',
		'iconst_0',
		'aload_0',
		['getfield', c_name, 'blockEntity', 'Lcom/thebluetropics/crabpack/SmelterBlockEntity;'],
		['getfield', 'com/thebluetropics/crabpack/SmelterBlockEntity', 'cookTime', 'I'],
		['invokeinterface', 'cp', 'a', '(Lcl;II)V', 4],

		'aload_1',
		'aload_0',
		'iconst_1',
		'aload_0',
		['getfield', c_name, 'blockEntity', 'Lcom/thebluetropics/crabpack/SmelterBlockEntity;'],
		['getfield', 'com/thebluetropics/crabpack/SmelterBlockEntity', 'burnTime', 'I'],
		['invokeinterface', 'cp', 'a', '(Lcl;II)V', 4],

		'aload_1',
		'aload_0',
		'iconst_2',
		'aload_0',
		['getfield', c_name, 'blockEntity', 'Lcom/thebluetropics/crabpack/SmelterBlockEntity;'],
		['getfield', 'com/thebluetropics/crabpack/SmelterBlockEntity', 'fuelTime', 'I'],
		['invokeinterface', 'cp', 'a', '(Lcl;II)V', 4],

		'return'
	])
	a_code = a_code_assemble([
		(4).to_bytes(2),
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

def _create_quick_move_method(cf, cp_cache, side, c_name):
	m = create_method(cf, cp_cache, ['public'], 'a', ['(I)Liz;', '(I)Lfy;'][side])

	code = assemble_code(cf, cp_cache, 0, 0, [
		'aconst_null',
		['astore', 2],

		'aload_0',
		['getfield', c_name, 'e', 'Ljava/util/List;'],
		['iload', 1],
		['invokeinterface', 'java/util/List', 'get', '(I)Ljava/lang/Object;', 2],
		['checkcast', ('gp', 'el')],
		['astore', 3],

		['aload', 3],
		['ifnull', 'L3'],
		['aload', 3],
		['invokevirtual', ('gp', 'el'), 'b', '()Z'],
		['ifeq', 'L3'],

		['label', 'L4'],
		['aload', 3],
		['invokevirtual', ('gp', 'el'), 'a', ('()Liz;', '()Lfy;')],
		['astore', 4],

		['aload', 4],
		['invokevirtual', ('iz', 'fy'), ('k', 'j'), ('()Liz;', '()Lfy;')],
		['astore', 2],

		['iload', 1],
		'iconst_2',
		['if_icmpne', 'L7'],

		['label', 'L8'],
		'aload_0',
		['aload', 4],
		'iconst_3',
		['bipush', 39],
		'iconst_1',
		['invokevirtual', c_name, 'a', ('(Liz;IIZ)V', '(Lfy;IIZ)V')],
		['goto', 'L9'],

		['label', 'L7'],
		['iload', 1],
		'iconst_3',
		['if_icmplt', 'L10'],
		['iload', 1],
		['bipush', 30],
		['if_icmpge', 'L10'],

		['label', 'L11'],
		'aload_0',
		['aload', 4],
		['bipush', 30],
		['bipush', 39],
		'iconst_0',
		['invokevirtual', c_name, 'a', ('(Liz;IIZ)V', '(Lfy;IIZ)V')],
		['goto', 'L9'],

		['label', 'L10'],
		['iload', 1],
		['bipush', 30],
		['if_icmplt', 'L12'],
		['iload', 1],
		['bipush', 39],
		['if_icmpge', 'L12'],

		['label', 'L13'],
		'aload_0',
		['aload', 4],
		'iconst_3',
		['bipush', 30],
		'iconst_0',
		['invokevirtual', c_name, 'a', ('(Liz;IIZ)V', '(Lfy;IIZ)V')],
		['goto', 'L9'],

		['label', 'L12'],
		'aload_0',
		['aload', 4],
		'iconst_3',
		['bipush', 39],
		'iconst_0',
		['invokevirtual', c_name, 'a', ('(Liz;IIZ)V', '(Lfy;IIZ)V')],

		['label', 'L9'],
		['aload', 4],
		['getfield', ('iz', 'fy'), 'a', 'I'],
		['ifne', 'L14'],

		['label', 'L15'],
		['aload', 3],
		'aconst_null',
		['invokevirtual', ('gp', 'el'), 'c', ('(Liz;)V', '(Lfy;)V')],
		['goto', 'L16'],

		['label', 'L14'],
		['aload', 3],
		['invokevirtual', ('gp', 'el'), 'c', '()V'],

		['label', 'L16'],
		['aload', 4],
		['getfield', ('iz', 'fy'), 'a', 'I'],
		['aload', 2],
		['getfield', ('iz', 'fy'), 'a', 'I'],
		['if_icmpeq', 'L17'],

		['label', 'L18'],
		['aload', 3],
		['aload', 4],
		['invokevirtual', ('gp', 'el'), 'a', ('(Liz;)V', '(Lfy;)V')],
		['goto', 'L3'],

		['label', 'L17'],
		'aconst_null',
		'areturn',

		['label', 'L3'],
		['aload', 2],
		'areturn'
	])
	a_code = a_code_assemble([
		(5).to_bytes(2),
		(5).to_bytes(2),
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
