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

def apply():
	c_name = 'com/thebluetropics/crabpack/SmelterScreen'

	cf = cf_create()
	cp_cache = cp_init_cache(cf[0x04])

	cf[0x02] = (49).to_bytes(2)

	cf[0x05] = (0x0001.__or__(0x0020)).to_bytes(2)
	cf[0x06] = i2cpx_c(cf, cp_cache, c_name)
	cf[0x07] = i2cpx_c(cf, cp_cache, 'id')

	cf[0x0b].append(create_field(cf, cp_cache, ['private'], 'blockEntity', 'Lcom/thebluetropics/crabpack/SmelterBlockEntity;'))
	cf[0x0a] = len(cf[0x0b]).to_bytes(2)

	cf[0x0d].append(_create_constructor(cf, cp_cache, c_name))
	cf[0x0d].append(_create_draw_background_method(cf, cp_cache, c_name))
	cf[0x0c] = len(cf[0x0d]).to_bytes(2)

	if not os.path.exists('stage/client/com/thebluetropics/crabpack'):
		os.makedirs('stage/client/com/thebluetropics/crabpack', exist_ok=True)

	with open(mod.config.path(f'stage/client/{c_name}.class'), 'wb') as file:
		file.write(cf_assemble(cf))

	print(f'Created client:SmelterScreen.class')

def _create_constructor(cf, cp_cache, c_name):
	m = create_method(cf, cp_cache, ['public'], '<init>', '(Lix;Lcom/thebluetropics/crabpack/SmelterBlockEntity;)V')

	code = assemble_code(cf, cp_cache, 0, 0, [
		'aload_0',
		['new', 'com/thebluetropics/crabpack/SmelterScreenHandler'],
		'dup',
		'aload_1',
		'aload_2',
		['invokespecial', 'com/thebluetropics/crabpack/SmelterScreenHandler', '<init>', '(Lix;Lcom/thebluetropics/crabpack/SmelterBlockEntity;)V'],
		['invokespecial', 'id', '<init>', '(Ldw;)V'],
		'aload_0',
		'aload_2',
		['putfield', c_name, 'blockEntity', 'Lcom/thebluetropics/crabpack/SmelterBlockEntity;'],
		'aload_0', ['sipush', 176], ['putfield', c_name, 'a', 'I'],
		'aload_0', ['sipush', 156], ['putfield', c_name, 'i', 'I'],
		'return'
	])
	a_code = a_code_assemble([
		(5).to_bytes(2),
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

def _create_draw_background_method(cf, cp_cache, c_name):
	m = create_method(cf, cp_cache, ['public'], 'a', '(F)V')

	code = assemble_code(cf, cp_cache, 0, 0, [
		'aload_0',
		['getfield', c_name, 'b', 'Lnet/minecraft/client/Minecraft;'],
		['getfield', 'net/minecraft/client/Minecraft', 'p', 'Lji;'],
		['ldc.string', '/gui/smelter.png'],
		['invokevirtual', 'ji', 'b', '(Ljava/lang/String;)I'],
		['istore', 2],

		'fconst_1',
		'fconst_1',
		'fconst_1',
		'fconst_1',
		['invokestatic', 'org/lwjgl/opengl/GL11', 'glColor4f', '(FFFF)V'],

		'aload_0',
		['getfield', c_name, 'b', 'Lnet/minecraft/client/Minecraft;'],
		['getfield', 'net/minecraft/client/Minecraft', 'p', 'Lji;'],
		['iload', 2],
		['invokevirtual', 'ji', 'b', '(I)V'],

		'aload_0',
		['getfield', c_name, 'c', 'I'],
		'aload_0',
		['getfield', c_name, 'a', 'I'],
		'isub',
		'iconst_2',
		'idiv',
		['istore', 3],

		'aload_0',
		['getfield', c_name, 'd', 'I'],
		'aload_0',
		['getfield', c_name, 'i', 'I'],
		'isub',
		'iconst_2',
		'idiv',
		['istore', 4],

		'aload_0',
		['iload', 3],
		['iload', 4],
		'iconst_0',
		'iconst_0',
		'aload_0',
		['getfield', c_name, 'a', 'I'],
		'aload_0',
		['getfield', c_name, 'i', 'I'],
		['invokevirtual', c_name, 'b', '(IIIIII)V'],

		['label', 'L6'],
		'aload_0',
		['getfield', c_name, 'blockEntity', 'Lcom/thebluetropics/crabpack/SmelterBlockEntity;'],
		['invokevirtual', 'com/thebluetropics/crabpack/SmelterBlockEntity', 'isBurning', '()Z'],
		['ifeq', 'L7'],

		['label', 'L8'],
		'aload_0',
		['getfield', c_name, 'blockEntity', 'Lcom/thebluetropics/crabpack/SmelterBlockEntity;'],
		['bipush', 12],
		['invokevirtual', 'com/thebluetropics/crabpack/SmelterBlockEntity', 'getFuelTimeDelta', '(I)I'],
		['istore', 5],

		['label', 'L9'],
		'aload_0',
		['iload', 3],
		['bipush', 51],
		'iadd',
		['iload', 4],
		['bipush', 31],
		'iadd',
		['bipush', 12],
		'iadd',
		['iload', 5],
		'isub',
		['sipush', 176],
		['bipush', 12],
		['iload', 5],
		'isub',
		['bipush', 14],
		['iload', 5],
		'iconst_2',
		'iadd',
		['invokevirtual', c_name, 'b', '(IIIIII)V'],

		['label', 'L7'],
		'aload_0',
		['getfield', c_name, 'blockEntity', 'Lcom/thebluetropics/crabpack/SmelterBlockEntity;'],
		['bipush', 25],
		['invokevirtual', 'com/thebluetropics/crabpack/SmelterBlockEntity', 'getCookTimeDelta', '(I)I'],
		['istore', 5],

		['label', 'L10'],
		'aload_0',
		['iload', 3],
		['bipush', 76],
		'iadd',
		['iload', 4],
		['bipush', 29],
		'iadd',
		['sipush', 176],
		['bipush', 14],
		['iload', 5],
		'iconst_1',
		'iadd',
		['bipush', 16],
		['invokevirtual', c_name, 'b', '(IIIIII)V'],

		['label', 'L11'],

		'return'
	])
	a_code = a_code_assemble([
		(8).to_bytes(2),
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
