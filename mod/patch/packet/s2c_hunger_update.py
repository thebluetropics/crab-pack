import os, mod

from mod.field import create_field
from mod.method import create_method
from mod import (
	attribute,
	instructions,
	constant_pool
)
from mod.class_file import (
	create_class_file,
	assemble_class_file
)
from mod.constant_pool import (
	icpx_f,
	icpx_m,
	i2cpx_utf8,
	i2cpx_c
)

def apply(side_name):
	if not mod.config.is_feature_enabled('experimental.hunger_and_thirst'):
		return

	side = 0 if side_name.__eq__('client') else 1
	c_name = 'com/thebluetropics/crabpack/HungerUpdatePacket'

	cf = create_class_file()
	cp_cache = constant_pool.init_constant_pool_cache(cf[0x04])

	cf[0x05] = (0x0001.__or__(0x0020)).to_bytes(2)
	cf[0x06] = i2cpx_c(cf, cp_cache, c_name)
	cf[0x07] = i2cpx_c(cf, cp_cache, ['ki', 'gt'][side])

	fields = [
		create_field(cf, cp_cache, ['public'], 'hunger', 'I'),
		create_field(cf, cp_cache, ['public'], 'maxHunger', 'I')
	]
	cf[0x0a], cf[0x0b] = (len(fields).to_bytes(2), fields)

	methods = [
		_create_constructor_a(cf, cp_cache, side),
		_create_constructor_b(cf, cp_cache, side),
		_create_read_method(cf, cp_cache),
		_create_write_method(cf, cp_cache),
		_create_apply_method(cf, cp_cache, side),
		_create_size_method(cf, cp_cache)
	]
	cf[0x0c], cf[0x0d] = (len(methods).to_bytes(2), methods)

	if not os.path.exists(f'stage/{side_name}/com/thebluetropics/crabpack'):
		os.makedirs(f'stage/{side_name}/com/thebluetropics/crabpack', exist_ok=True)

	with open(mod.config.path(f'stage/{side_name}/{c_name}.class'), 'wb') as file:
		file.write(assemble_class_file(cf))

	print(f'Created {side_name}:HungerUpdatePacket.class')

def _create_constructor_a(cf, cp_cache, side):
	m = create_method(cf, cp_cache, ['public'], '<init>', '()V')

	code = instructions.assemble(0, [
		'aload_0', ['invokespecial', icpx_m(cf, cp_cache, ['ki', 'gt'][side], '<init>', '()V')],
		'return'
	])
	a_code = attribute.code.assemble([
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

	code = instructions.assemble(0, [
		'aload_0', ['invokespecial', icpx_m(cf, cp_cache, ['ki', 'gt'][side], '<init>', '()V')],
		'aload_0', ['iload_1'], ['putfield', icpx_f(cf, cp_cache, 'com/thebluetropics/crabpack/HungerUpdatePacket', 'hunger', 'I')],
		'aload_0', ['iload_2'], ['putfield', icpx_f(cf, cp_cache, 'com/thebluetropics/crabpack/HungerUpdatePacket', 'maxHunger', 'I')],
		'return'
	])
	a_code = attribute.code.assemble([
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

def _create_read_method(cf, cp_cache):
	m = create_method(cf, cp_cache, ['public'], 'a', '(Ljava/io/DataInputStream;)V')

	code = instructions.assemble(0, [
		'aload_0',
		'aload_1', ['invokevirtual', icpx_m(cf, cp_cache, 'java/io/DataInputStream', 'readShort', '()S')],
		['putfield', icpx_f(cf, cp_cache, 'com/thebluetropics/crabpack/HungerUpdatePacket', 'hunger', 'I')],
		'aload_0',
		'aload_1', ['invokevirtual', icpx_m(cf, cp_cache, 'java/io/DataInputStream', 'readShort', '()S')],
		['putfield', icpx_f(cf, cp_cache, 'com/thebluetropics/crabpack/HungerUpdatePacket', 'maxHunger', 'I')],
		'return'
	])
	a_code = attribute.code.assemble([
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

def _create_write_method(cf, cp_cache):
	m = create_method(cf, cp_cache, ['public'], 'a', '(Ljava/io/DataOutputStream;)V')

	code = instructions.assemble(0, [
		'aload_1',
		'aload_0', ['getfield', icpx_f(cf, cp_cache, 'com/thebluetropics/crabpack/HungerUpdatePacket', 'hunger', 'I')],
		['invokevirtual', icpx_m(cf, cp_cache, 'java/io/DataOutputStream', 'writeShort', '(I)V')],
		'aload_1',
		'aload_0', ['getfield', icpx_f(cf, cp_cache, 'com/thebluetropics/crabpack/HungerUpdatePacket', 'maxHunger', 'I')],
		['invokevirtual', icpx_m(cf, cp_cache, 'java/io/DataOutputStream', 'writeShort', '(I)V')],
		'return'
	])
	a_code = attribute.code.assemble([
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

	code = instructions.assemble(0, [
		'aload_1',
		'aload_0',
		['invokevirtual', icpx_m(cf, cp_cache, ['ti', 'me'][side], 'onHungerUpdate', '(Lcom/thebluetropics/crabpack/HungerUpdatePacket;)V')],
		'return'
	])
	a_code = attribute.code.assemble([
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

def _create_size_method(cf, cp_cache):
	m = create_method(cf, cp_cache, ['public'], 'a', '()I')

	code = instructions.assemble(0, [
		'iconst_4',
		'ireturn'
	])
	a_code = attribute.code.assemble([
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
