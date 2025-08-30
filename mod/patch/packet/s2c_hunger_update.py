import os, mod

from mod.jvm import (
	class_file,
	attribute,
	instructions,
	constant_pool,
	create_field,
	create_method,
	icpx_f,
	i2cpx_c,
	icpx_m,
	i2cpx_utf8
)

def apply_client():
	cf = class_file.create_new()
	xcp = constant_pool.use_helper(cf)

	cf[0x05] = (0x0001.__or__(0x0020)).to_bytes(2)
	cf[0x06] = i2cpx_c(xcp, 'com/thebluetropics/crabpack/HungerUpdatePacket')
	cf[0x07] = i2cpx_c(xcp, 'ki')

	fields = [
		create_field(xcp, ['public'], 'hunger', 'I'),
		create_field(xcp, ['public'], 'maxHunger', 'I')
	]
	cf[0x0a], cf[0x0b] = (len(fields).to_bytes(2), fields)

	methods = [
		_client_empty_constructor(xcp),
		_client_constructor(xcp),
		_client_read(xcp),
		_client_write(xcp),
		_client_apply(xcp),
		_client_size(xcp)
	]
	cf[0x0c], cf[0x0d] = (len(methods).to_bytes(2), methods)

	if not os.path.exists('stage/client/com/thebluetropics/crabpack'):
		os.makedirs('stage/client/com/thebluetropics/crabpack', exist_ok=True)

	with open(mod.config.path('stage/client/com/thebluetropics/crabpack/HungerUpdatePacket.class'), 'wb') as file:
		file.write(class_file.assemble(cf))

	print('Created client:HungerUpdatePacket.class')

def _client_empty_constructor(xcp):
	m = create_method(xcp, ['public'], '<init>', '()V')

	code = instructions.assemble(0, [
		'aload_0', ['invokespecial', icpx_m(xcp, 'ki', '<init>', '()V')],
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
	m[0x04] = [[i2cpx_utf8(xcp, 'Code'), len(a_code).to_bytes(4), a_code]]

	return m

def _client_constructor(xcp):
	m = create_method(xcp, ['public'], '<init>', '(II)V')

	code = instructions.assemble(0, [
		'aload_0', ['invokespecial', icpx_m(xcp, 'ki', '<init>', '()V')],
		'aload_0', ['iload_1'], ['putfield', icpx_f(xcp, 'com/thebluetropics/crabpack/HungerUpdatePacket', 'hunger', 'I')],
		'aload_0', ['iload_2'], ['putfield', icpx_f(xcp, 'com/thebluetropics/crabpack/HungerUpdatePacket', 'maxHunger', 'I')],
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
	m[0x04] = [[i2cpx_utf8(xcp, 'Code'), len(a_code).to_bytes(4), a_code]]

	return m

def _client_read(xcp):
	m = create_method(xcp, ['public'], 'a', '(Ljava/io/DataInputStream;)V')

	code = instructions.assemble(0, [
		'aload_0',
		'aload_1', ['invokevirtual', icpx_m(xcp, 'java/io/DataInputStream', 'readShort', '()S')],
		['putfield', icpx_f(xcp, 'com/thebluetropics/crabpack/HungerUpdatePacket', 'hunger', 'I')],
		'aload_0',
		'aload_1', ['invokevirtual', icpx_m(xcp, 'java/io/DataInputStream', 'readShort', '()S')],
		['putfield', icpx_f(xcp, 'com/thebluetropics/crabpack/HungerUpdatePacket', 'maxHunger', 'I')],
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
	m[0x04] = [[i2cpx_utf8(xcp, 'Code'), len(a_code).to_bytes(4), a_code]]

	return m

def _client_write(xcp):
	m = create_method(xcp, ['public'], 'a', '(Ljava/io/DataOutputStream;)V')

	code = instructions.assemble(0, [
		'aload_1',
		'aload_0', ['getfield', icpx_f(xcp, 'com/thebluetropics/crabpack/HungerUpdatePacket', 'hunger', 'I')],
		['invokevirtual', icpx_m(xcp, 'java/io/DataOutputStream', 'writeShort', '(I)V')],
		'aload_1',
		'aload_0', ['getfield', icpx_f(xcp, 'com/thebluetropics/crabpack/HungerUpdatePacket', 'maxHunger', 'I')],
		['invokevirtual', icpx_m(xcp, 'java/io/DataOutputStream', 'writeShort', '(I)V')],
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
	m[0x04] = [[i2cpx_utf8(xcp, 'Code'), len(a_code).to_bytes(4), a_code]]

	return m

def _client_apply(xcp):
	m = create_method(xcp, ['public'], 'a', '(Lti;)V')

	code = instructions.assemble(0, [
		'aload_1',
		'aload_0',
		['invokevirtual', icpx_m(xcp, 'ti', 'onHungerUpdate', '(Lcom/thebluetropics/crabpack/HungerUpdatePacket;)V')],
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
	m[0x04] = [[i2cpx_utf8(xcp, 'Code'), len(a_code).to_bytes(4), a_code]]

	return m

def _client_size(xcp):
	m = create_method(xcp, ['public'], 'a', '()I')

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
	m[0x04] = [[i2cpx_utf8(xcp, 'Code'), len(a_code).to_bytes(4), a_code]]

	return m

def apply_server():
	cf = class_file.create_new()
	xcp = constant_pool.use_helper(cf)

	cf[0x05] = (0x0001.__or__(0x0020)).to_bytes(2)
	cf[0x06] = i2cpx_c(xcp, 'com/thebluetropics/crabpack/HungerUpdatePacket')
	cf[0x07] = i2cpx_c(xcp, 'gt')

	fields = [
		create_field(xcp, ['public'], 'hunger', 'I'),
		create_field(xcp, ['public'], 'maxHunger', 'I')
	]
	cf[0x0a], cf[0x0b] = (len(fields).to_bytes(2), fields)

	methods = [
		_server_empty_constructor(xcp),
		_server_constructor(xcp),
		_server_read(xcp),
		_server_write(xcp),
		_server_apply(xcp),
		_server_size(xcp)
	]
	cf[0x0c], cf[0x0d] = (len(methods).to_bytes(2), methods)

	if not os.path.exists('stage/server/com/thebluetropics/crabpack'):
		os.makedirs('stage/server/com/thebluetropics/crabpack', exist_ok=True)

	with open(mod.config.path('stage/server/com/thebluetropics/crabpack/HungerUpdatePacket.class'), 'wb') as file:
		file.write(class_file.assemble(cf))

	print('Created server:HungerUpdatePacket.class')

def _server_empty_constructor(xcp):
	m = create_method(xcp, ['public'], '<init>', '()V')

	code = instructions.assemble(0, [
		'aload_0', ['invokespecial', icpx_m(xcp, 'gt', '<init>', '()V')],
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
	m[0x04] = [[i2cpx_utf8(xcp, 'Code'), len(a_code).to_bytes(4), a_code]]

	return m

def _server_constructor(xcp):
	m = create_method(xcp, ['public'], '<init>', '(II)V')

	code = instructions.assemble(0, [
		'aload_0', ['invokespecial', icpx_m(xcp, 'gt', '<init>', '()V')],
		'aload_0', ['iload_1'], ['putfield', icpx_f(xcp, 'com/thebluetropics/crabpack/HungerUpdatePacket', 'hunger', 'I')],
		'aload_0', ['iload_2'], ['putfield', icpx_f(xcp, 'com/thebluetropics/crabpack/HungerUpdatePacket', 'maxHunger', 'I')],
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
	m[0x04] = [[i2cpx_utf8(xcp, 'Code'), len(a_code).to_bytes(4), a_code]]

	return m

def _server_read(xcp):
	m = create_method(xcp, ['public'], 'a', '(Ljava/io/DataInputStream;)V')

	code = instructions.assemble(0, [
		'aload_0',
		'aload_1', ['invokevirtual', icpx_m(xcp, 'java/io/DataInputStream', 'readShort', '()S')],
		['putfield', icpx_f(xcp, 'com/thebluetropics/crabpack/HungerUpdatePacket', 'hunger', 'I')],
		'aload_0',
		'aload_1', ['invokevirtual', icpx_m(xcp, 'java/io/DataInputStream', 'readShort', '()S')],
		['putfield', icpx_f(xcp, 'com/thebluetropics/crabpack/HungerUpdatePacket', 'maxHunger', 'I')],
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
	m[0x04] = [[i2cpx_utf8(xcp, 'Code'), len(a_code).to_bytes(4), a_code]]

	return m

def _server_write(xcp):
	m = create_method(xcp, ['public'], 'a', '(Ljava/io/DataOutputStream;)V')

	code = instructions.assemble(0, [
		'aload_1',
		'aload_0', ['getfield', icpx_f(xcp, 'com/thebluetropics/crabpack/HungerUpdatePacket', 'hunger', 'I')],
		['invokevirtual', icpx_m(xcp, 'java/io/DataOutputStream', 'writeShort', '(I)V')],
		'aload_1',
		'aload_0', ['getfield', icpx_f(xcp, 'com/thebluetropics/crabpack/HungerUpdatePacket', 'maxHunger', 'I')],
		['invokevirtual', icpx_m(xcp, 'java/io/DataOutputStream', 'writeShort', '(I)V')],
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
	m[0x04] = [[i2cpx_utf8(xcp, 'Code'), len(a_code).to_bytes(4), a_code]]

	return m

def _server_apply(xcp):
	m = create_method(xcp, ['public'], 'a', '(Lme;)V')

	code = instructions.assemble(0, [
		'aload_1',
		'aload_0',
		['invokevirtual', icpx_m(xcp, 'me', 'onHungerUpdate', '(Lcom/thebluetropics/crabpack/HungerUpdatePacket;)V')],
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
	m[0x04] = [[i2cpx_utf8(xcp, 'Code'), len(a_code).to_bytes(4), a_code]]

	return m

def _server_size(xcp):
	m = create_method(xcp, ['public'], 'a', '()I')

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
	m[0x04] = [[i2cpx_utf8(xcp, 'Code'), len(a_code).to_bytes(4), a_code]]

	return m
