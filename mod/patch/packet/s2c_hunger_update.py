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
from modmaker.m import (
	create_method
)
from modmaker.f import (
	create_field
)

def apply(side_name):
	if not mod.config.is_feature_enabled('etc.hunger_and_thirst'):
		return

	side = 0 if side_name.__eq__('client') else 1
	c_name = 'com/thebluetropics/crabpack/HungerUpdatePacket'

	cf = cf_create()
	cp_cache = cp_init_cache(cf[0x04])

	cf[0x05] = (0x0001.__or__(0x0020)).to_bytes(2)
	cf[0x06] = i2cpx_c(cf, cp_cache, c_name)
	cf[0x07] = i2cpx_c(cf, cp_cache, ['ki', 'gt'][side])

	cf[0x0b].append(create_field(cf, cp_cache, ['public'], 'hunger', 'I'))
	cf[0x0b].append(create_field(cf, cp_cache, ['public'], 'maxHunger', 'I'))
	cf[0x0a] = len(cf[0x0b]).to_bytes(2)

	cf[0x0d].append(_create_constructor_a(cf, cp_cache, side))
	cf[0x0d].append(_create_constructor_b(cf, cp_cache, side))
	cf[0x0d].append(_create_read_method(cf, cp_cache, side))
	cf[0x0d].append(_create_write_method(cf, cp_cache, side))
	cf[0x0d].append(_create_apply_method(cf, cp_cache, side))
	cf[0x0d].append(_create_size_method(cf, cp_cache, side))
	cf[0x0c] = len(cf[0x0d]).to_bytes(2)

	if not os.path.exists(f'stage/{side_name}/com/thebluetropics/crabpack'):
		os.makedirs(f'stage/{side_name}/com/thebluetropics/crabpack', exist_ok=True)

	with open(mod.config.path(f'stage/{side_name}/{c_name}.class'), 'wb') as file:
		file.write(cf_assemble(cf))

	print(f'Created {side_name}:HungerUpdatePacket.class')

def _create_constructor_a(cf, cp_cache, side):
	m = create_method(cf, cp_cache, ['public'], '<init>', '()V')

	code = assemble_code(cf, cp_cache, side, 0, [
		'aload_0', ['invokespecial', ('ki', 'gt'), '<init>', '()V'],
		'return'
	])
	a_code = a_code_assemble([
		(1).to_bytes(2),
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

def _create_constructor_b(cf, cp_cache, side):
	m = create_method(cf, cp_cache, ['public'], '<init>', '(II)V')

	code = assemble_code(cf, cp_cache, side, 0, [
		'aload_0', ['invokespecial', ('ki', 'gt'), '<init>', '()V'],
		'aload_0', 'iload_1', ['putfield', 'com/thebluetropics/crabpack/HungerUpdatePacket', 'hunger', 'I'],
		'aload_0', 'iload_2', ['putfield', 'com/thebluetropics/crabpack/HungerUpdatePacket', 'maxHunger', 'I'],
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

def _create_read_method(cf, cp_cache, side):
	m = create_method(cf, cp_cache, ['public'], 'a', '(Ljava/io/DataInputStream;)V')

	code = assemble_code(cf, cp_cache, side, 0, [
		'aload_0',
		'aload_1', ['invokevirtual', 'java/io/DataInputStream', 'readShort', '()S'],
		['putfield', 'com/thebluetropics/crabpack/HungerUpdatePacket', 'hunger', 'I'],
		'aload_0',
		'aload_1', ['invokevirtual', 'java/io/DataInputStream', 'readShort', '()S'],
		['putfield', 'com/thebluetropics/crabpack/HungerUpdatePacket', 'maxHunger', 'I'],
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

def _create_write_method(cf, cp_cache, side):
	m = create_method(cf, cp_cache, ['public'], 'a', '(Ljava/io/DataOutputStream;)V')

	code = assemble_code(cf, cp_cache, side, 0, [
		'aload_1',
		'aload_0', ['getfield', 'com/thebluetropics/crabpack/HungerUpdatePacket', 'hunger', 'I'],
		['invokevirtual', 'java/io/DataOutputStream', 'writeShort', '(I)V'],
		'aload_1',
		'aload_0', ['getfield', 'com/thebluetropics/crabpack/HungerUpdatePacket', 'maxHunger', 'I'],
		['invokevirtual', 'java/io/DataOutputStream', 'writeShort', '(I)V'],
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

def _create_apply_method(cf, cp_cache, side):
	m = create_method(cf, cp_cache, ['public'], 'a', ['(Lti;)V', '(Lme;)V'][side])

	code = assemble_code(cf, cp_cache, side, 0, [
		'aload_1',
		'aload_0',
		['invokevirtual', ('ti', 'me'), 'onHungerUpdate', '(Lcom/thebluetropics/crabpack/HungerUpdatePacket;)V'],
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

def _create_size_method(cf, cp_cache, side):
	m = create_method(cf, cp_cache, ['public'], 'a', '()I')

	code = assemble_code(cf, cp_cache, side, 0, [
		'iconst_4',
		'ireturn'
	])
	a_code = a_code_assemble([
		(1).to_bytes(2),
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
