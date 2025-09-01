import os, mod

from mod.field import create_field
from mod.method import create_method
from mod import (
	class_file,
	attribute,
	instructions,
	constant_pool
)
from mod.constant_pool import (
	icpx_f,
	icpx_m,
	i2cpx_utf8,
	i2cpx_c
)

def apply_client():
	cf = class_file.create_new()
	cp_cache = constant_pool.init_constant_pool_cache(cf[0x04])

	cf[0x05] = (0x0001.__or__(0x0020)).to_bytes(2)
	cf[0x06] = i2cpx_c(cf, cp_cache, 'com/thebluetropics/crabpack/HungerUpdatePacket')
	cf[0x07] = i2cpx_c(cf, cp_cache, 'ki')

	fields = [
		create_field(cf, cp_cache, ['public'], 'hunger', 'I'),
		create_field(cf, cp_cache, ['public'], 'maxHunger', 'I')
	]
	cf[0x0a], cf[0x0b] = (len(fields).to_bytes(2), fields)

	methods = [
		_client_empty_constructor(cf, cp_cache),
		_client_constructor(cf, cp_cache),
		_client_read(cf, cp_cache),
		_client_write(cf, cp_cache),
		_client_apply(cf, cp_cache),
		_client_size(cf, cp_cache)
	]
	cf[0x0c], cf[0x0d] = (len(methods).to_bytes(2), methods)

	if not os.path.exists('stage/client/com/thebluetropics/crabpack'):
		os.makedirs('stage/client/com/thebluetropics/crabpack', exist_ok=True)

	with open(mod.config.path('stage/client/com/thebluetropics/crabpack/HungerUpdatePacket.class'), 'wb') as file:
		file.write(class_file.assemble(cf))

	print('Created client:HungerUpdatePacket.class')

def _client_empty_constructor(cf, cp_cache):
	m = create_method(cf, cp_cache, ['public'], '<init>', '()V')

	code = instructions.assemble(0, [
		'aload_0', ['invokespecial', icpx_m(cf, cp_cache, 'ki', '<init>', '()V')],
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

def _client_constructor(cf, cp_cache):
	m = create_method(cf, cp_cache, ['public'], '<init>', '(II)V')

	code = instructions.assemble(0, [
		'aload_0', ['invokespecial', icpx_m(cf, cp_cache, 'ki', '<init>', '()V')],
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

def _client_read(cf, cp_cache):
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

def _client_write(cf, cp_cache):
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

def _client_apply(cf, cp_cache):
	m = create_method(cf, cp_cache, ['public'], 'a', '(Lti;)V')

	code = instructions.assemble(0, [
		'aload_1',
		'aload_0',
		['invokevirtual', icpx_m(cf, cp_cache, 'ti', 'onHungerUpdate', '(Lcom/thebluetropics/crabpack/HungerUpdatePacket;)V')],
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

def _client_size(cf, cp_cache):
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

def apply_server():
	cf = class_file.create_new()
	cp_cache = constant_pool.init_constant_pool_cache(cf[0x04])

	cf[0x05] = (0x0001.__or__(0x0020)).to_bytes(2)
	cf[0x06] = i2cpx_c(cf, cp_cache, 'com/thebluetropics/crabpack/HungerUpdatePacket')
	cf[0x07] = i2cpx_c(cf, cp_cache, 'gt')

	fields = [
		create_field(cf, cp_cache, ['public'], 'hunger', 'I'),
		create_field(cf, cp_cache, ['public'], 'maxHunger', 'I')
	]
	cf[0x0a], cf[0x0b] = (len(fields).to_bytes(2), fields)

	methods = [
		_server_empty_constructor(cf, cp_cache),
		_server_constructor(cf, cp_cache),
		_server_read(cf, cp_cache),
		_server_write(cf, cp_cache),
		_server_apply(cf, cp_cache),
		_server_size(cf, cp_cache)
	]
	cf[0x0c], cf[0x0d] = (len(methods).to_bytes(2), methods)

	if not os.path.exists('stage/server/com/thebluetropics/crabpack'):
		os.makedirs('stage/server/com/thebluetropics/crabpack', exist_ok=True)

	with open(mod.config.path('stage/server/com/thebluetropics/crabpack/HungerUpdatePacket.class'), 'wb') as file:
		file.write(class_file.assemble(cf))

	print('Created server:HungerUpdatePacket.class')

def _server_empty_constructor(cf, cp_cache):
	m = create_method(cf, cp_cache, ['public'], '<init>', '()V')

	code = instructions.assemble(0, [
		'aload_0', ['invokespecial', icpx_m(cf, cp_cache, 'gt', '<init>', '()V')],
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

def _server_constructor(cf, cp_cache):
	m = create_method(cf, cp_cache, ['public'], '<init>', '(II)V')

	code = instructions.assemble(0, [
		'aload_0', ['invokespecial', icpx_m(cf, cp_cache, 'gt', '<init>', '()V')],
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

def _server_read(cf, cp_cache):
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

def _server_write(cf, cp_cache):
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

def _server_apply(cf, cp_cache):
	m = create_method(cf, cp_cache, ['public'], 'a', '(Lme;)V')

	code = instructions.assemble(0, [
		'aload_1',
		'aload_0',
		['invokevirtual', icpx_m(cf, cp_cache, 'me', 'onHungerUpdate', '(Lcom/thebluetropics/crabpack/HungerUpdatePacket;)V')],
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

def _server_size(cf, cp_cache):
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
