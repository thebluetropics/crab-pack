import mod

from modmaker.a_code import (
	a_code_assemble,
	assemble_code
)
from modmaker.m import (
	create_method
)
from modmaker.cf import (
	load_class_file,
	cf_assemble
)
from modmaker.cp import (
	cp_init_cache,
	i2cpx_utf8
)

def apply():
	if not mod.config.is_feature_enabled('etc.hunger_and_thirst'):
		return

	cf = load_class_file(mod.config.path('stage/server/dl.class'))
	cp_cache = cp_init_cache(cf[0x04])

	cf[0x0c] = (int.from_bytes(cf[0x0c]) + 3).to_bytes(2)
	cf[0x0d].append(_create_update_hunger_method(cf, cp_cache))
	cf[0x0d].append(_create_update_thirst_method(cf, cp_cache))
	cf[0x0d].append(_create_open_smelter_screen_method(cf, cp_cache))

	with open('stage/server/dl.class', 'wb') as file:
		file.write(cf_assemble(cf))

	print('Patched server:dl.class → net.minecraft.entity.ServerPlayerEntity')

def _create_update_hunger_method(cf, cp_cache):
	m = create_method(cf, cp_cache, ['protected'], 'updateHunger', '(II)V')

	code = assemble_code(cf, cp_cache, 1, 0, [
		'aload_0',
		['getfield', 'dl', 'a', 'Lha;'],
		['new', 'com/thebluetropics/crabpack/HungerUpdatePacket'],
		'dup',
		'iload_1',
		'iload_2',
		['invokespecial', 'com/thebluetropics/crabpack/HungerUpdatePacket', '<init>', '(II)V'],
		['invokevirtual', 'ha', 'b', '(Lgt;)V'],
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
	a = [i2cpx_utf8(cf, cp_cache, 'Code'), len(a_code).to_bytes(4), a_code]

	m[0x03] = (1).to_bytes(2)
	m[0x04] = [a]

	return m

def _create_update_thirst_method(cf, cp_cache):
	m = create_method(cf, cp_cache, ['protected'], 'updateThirst', '(II)V')

	code = assemble_code(cf, cp_cache, 1, 0, [
		'aload_0',
		['getfield', 'dl', 'a', 'Lha;'],
		['new', 'com/thebluetropics/crabpack/ThirstUpdatePacket'],
		'dup',
		'iload_1',
		'iload_2',
		['invokespecial', 'com/thebluetropics/crabpack/ThirstUpdatePacket', '<init>', '(II)V'],
		['invokevirtual', 'ha', 'b', '(Lgt;)V'],
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

def _create_open_smelter_screen_method(cf, cp_cache):
	m = create_method(cf, cp_cache, ['public'], 'openSmelterScreen', '(Lcom/thebluetropics/crabpack/SmelterBlockEntity;)V')

	code = assemble_code(cf, cp_cache, 1, 0, [
		'aload_0',
		['invokespecial', 'dl', 'ai', '()V'],

		'aload_0',
		['getfield', 'dl', 'a', 'Lha;'],
		['new', 'fw'],
		'dup',
		'aload_0',
		['getfield', 'dl', 'bO', 'I'],
		'iconst_4',
		'aload_1',
		['invokevirtual', 'com/thebluetropics/crabpack/SmelterBlockEntity', 'c', '()Ljava/lang/String;'],
		'aload_1',
		['invokevirtual', 'com/thebluetropics/crabpack/SmelterBlockEntity', 'a', '()I'],
		['invokespecial', 'fw', '<init>', '(IILjava/lang/String;I)V'],
		['invokevirtual', 'ha', 'b', '(Lgt;)V'],

		'aload_0',
		['new', 'com/thebluetropics/crabpack/SmelterScreenHandler'],
		'dup',
		'aload_0',
		['getfield', 'dl', 'i', 'Lfx;'],
		'aload_1',
		['invokespecial', 'com/thebluetropics/crabpack/SmelterScreenHandler', '<init>', '(Lfx;Lcom/thebluetropics/crabpack/SmelterBlockEntity;)V'],
		['putfield', 'dl', 'k', 'Lcl;'],

		'aload_0',
		['getfield', 'dl', 'k', 'Lcl;'],
		'aload_0',
		['getfield', 'dl', 'bO', 'I'],
		['putfield', 'cl', 'f', 'I'],

		'aload_0',
		['getfield', 'dl', 'k', 'Lcl;'],
		'aload_0',
		['invokevirtual', 'cl', 'a', '(Lcp;)V'],

		'return'
	])
	a_code = a_code_assemble([
		(7).to_bytes(2),
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
