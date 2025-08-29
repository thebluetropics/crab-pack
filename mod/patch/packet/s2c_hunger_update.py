import os
import mod

from mod.bytecode import (
	class_file,
	code_attribute,
	instructions,
	utf8
)
from mod.bytecode.fields import make_field
from mod.bytecode.method import (make_method, get_method)
from mod.bytecode.attribute import get_attribute
from mod.bytecode import (
	class_file,
	code_attribute,
	instructions,
	constant_pool
)
from mod.bytecode.constant_pool import (
	icpx_utf8,
	i2cpx_c,
	icpx_f,
	icpx_m,
	i2cpx_utf8,
)

def apply_client():
	cf = class_file.create_template()
	xcp = constant_pool.use_helper(cf)

	cf[0x05] = (0x0001.__or__(0x0020)).to_bytes(2)
	cf[0x06] = i2cpx_c(xcp, 'com/thebluetropics/crabpack/HungerUpdatePacket')
	cf[0x07] = i2cpx_c(xcp, 'ki')

	fields = [
		make_field(['public'], icpx_utf8(xcp, 'hunger'), icpx_utf8(xcp, 'I')),
		make_field(['public'], icpx_utf8(xcp, 'maxHunger'), icpx_utf8(xcp, 'I'))
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

	if not os.path.exists("stage/client/com/thebluetropics/crabpack"):
		os.makedirs("stage/client/com/thebluetropics/crabpack", exist_ok=True)

	with open(mod.config.path("stage/client/com/thebluetropics/crabpack/HungerUpdatePacket.class"), "wb") as file:
		file.write(class_file.make(cf))

	print("Created client:HungerUpdatePacket.class")

def _client_empty_constructor(xcp):
	m = make_method(['public'], icpx_utf8(xcp, '<init>'), icpx_utf8(xcp, '()V'))

	code = instructions.make(0, [
		'aload_0', ['invokespecial', icpx_m(xcp, 'ki', '<init>', '()V')],
		'return'
	])
	a_code = code_attribute.assemble([
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
	m = make_method(['public'], icpx_utf8(xcp, '<init>'), icpx_utf8(xcp, '(II)V'))

	code = instructions.make(0, [
		'aload_0', ['invokespecial', icpx_m(xcp, 'ki', '<init>', '()V')],
		'aload_0', ['iload_1'], ['putfield', icpx_f(xcp, 'com/thebluetropics/crabpack/HungerUpdatePacket', 'hunger', 'I')],
		'aload_0', ['iload_2'], ['putfield', icpx_f(xcp, 'com/thebluetropics/crabpack/HungerUpdatePacket', 'maxHunger', 'I')],
		'return'
	])
	a_code = code_attribute.assemble([
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
	m = make_method(['public'], icpx_utf8(xcp, 'a'), icpx_utf8(xcp, '(Ljava/io/DataInputStream;)V'))

	code = instructions.make(0, [
		'aload_0',
		'aload_1', ['invokevirtual', icpx_m(xcp, 'java/io/DataInputStream', 'readShort', '()S')],
		['putfield', icpx_f(xcp, 'com/thebluetropics/crabpack/HungerUpdatePacket', 'hunger', 'I')],
		'aload_0',
		'aload_1', ['invokevirtual', icpx_m(xcp, 'java/io/DataInputStream', 'readShort', '()S')],
		['putfield', icpx_f(xcp, 'com/thebluetropics/crabpack/HungerUpdatePacket', 'maxHunger', 'I')],
		'return'
	])
	a_code = code_attribute.assemble([
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
	m = make_method(['public'], icpx_utf8(xcp, 'a'), icpx_utf8(xcp, '(Ljava/io/DataOutputStream;)V'))

	code = instructions.make(0, [
		'aload_1',
		'aload_0', ['getfield', icpx_f(xcp, 'com/thebluetropics/crabpack/HungerUpdatePacket', 'hunger', 'I')],
		['invokevirtual', icpx_m(xcp, 'java/io/DataOutputStream', 'writeShort', '(I)V')],
		'aload_1',
		'aload_0', ['getfield', icpx_f(xcp, 'com/thebluetropics/crabpack/HungerUpdatePacket', 'maxHunger', 'I')],
		['invokevirtual', icpx_m(xcp, 'java/io/DataOutputStream', 'writeShort', '(I)V')],
		'return'
	])
	a_code = code_attribute.assemble([
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
	m = make_method(['public'], icpx_utf8(xcp, 'a'), icpx_utf8(xcp, '(Lti;)V'))

	code = instructions.make(0, [
		'aload_1',
		'aload_0',
		['invokevirtual', icpx_m(xcp, 'ti', 'onHungerUpdate', '(Lcom/thebluetropics/crabpack/HungerUpdatePacket;)V')],
		'return'
	])
	a_code = code_attribute.assemble([
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
	m = make_method(['public'], icpx_utf8(xcp, 'a'), icpx_utf8(xcp, '()I'))

	code = instructions.make(0, [
		'iconst_4',
		'ireturn'
	])
	a_code = code_attribute.assemble([
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
	cf = class_file.create_template()
	xcp = constant_pool.use_helper(cf)

	cf[0x05] = (0x0001.__or__(0x0020)).to_bytes(2)
	cf[0x06] = i2cpx_c(xcp, 'com/thebluetropics/crabpack/HungerUpdatePacket')
	cf[0x07] = i2cpx_c(xcp, 'gt')

	fields = [
		make_field(['public'], icpx_utf8(xcp, 'hunger'), icpx_utf8(xcp, 'I')),
		make_field(['public'], icpx_utf8(xcp, 'maxHunger'), icpx_utf8(xcp, 'I'))
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

	if not os.path.exists("stage/server/com/thebluetropics/crabpack"):
		os.makedirs("stage/server/com/thebluetropics/crabpack", exist_ok=True)

	with open(mod.config.path("stage/server/com/thebluetropics/crabpack/HungerUpdatePacket.class"), "wb") as file:
		file.write(class_file.make(cf))

	print("Created server:HungerUpdatePacket.class")

def _server_empty_constructor(xcp):
	m = make_method(['public'], icpx_utf8(xcp, '<init>'), icpx_utf8(xcp, '()V'))

	code = instructions.make(0, [
		'aload_0', ['invokespecial', icpx_m(xcp, 'gt', '<init>', '()V')],
		'return'
	])
	a_code = code_attribute.assemble([
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
	m = make_method(['public'], icpx_utf8(xcp, '<init>'), icpx_utf8(xcp, '(II)V'))

	code = instructions.make(0, [
		'aload_0', ['invokespecial', icpx_m(xcp, 'gt', '<init>', '()V')],
		'aload_0', ['iload_1'], ['putfield', icpx_f(xcp, 'com/thebluetropics/crabpack/HungerUpdatePacket', 'hunger', 'I')],
		'aload_0', ['iload_2'], ['putfield', icpx_f(xcp, 'com/thebluetropics/crabpack/HungerUpdatePacket', 'maxHunger', 'I')],
		'return'
	])
	a_code = code_attribute.assemble([
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
	m = make_method(['public'], icpx_utf8(xcp, 'a'), icpx_utf8(xcp, '(Ljava/io/DataInputStream;)V'))

	code = instructions.make(0, [
		'aload_0',
		'aload_1', ['invokevirtual', icpx_m(xcp, 'java/io/DataInputStream', 'readShort', '()S')],
		['putfield', icpx_f(xcp, 'com/thebluetropics/crabpack/HungerUpdatePacket', 'hunger', 'I')],
		'aload_0',
		'aload_1', ['invokevirtual', icpx_m(xcp, 'java/io/DataInputStream', 'readShort', '()S')],
		['putfield', icpx_f(xcp, 'com/thebluetropics/crabpack/HungerUpdatePacket', 'maxHunger', 'I')],
		'return'
	])
	a_code = code_attribute.assemble([
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
	m = make_method(['public'], icpx_utf8(xcp, 'a'), icpx_utf8(xcp, '(Ljava/io/DataOutputStream;)V'))

	code = instructions.make(0, [
		'aload_1',
		'aload_0', ['getfield', icpx_f(xcp, 'com/thebluetropics/crabpack/HungerUpdatePacket', 'hunger', 'I')],
		['invokevirtual', icpx_m(xcp, 'java/io/DataOutputStream', 'writeShort', '(I)V')],
		'aload_1',
		'aload_0', ['getfield', icpx_f(xcp, 'com/thebluetropics/crabpack/HungerUpdatePacket', 'maxHunger', 'I')],
		['invokevirtual', icpx_m(xcp, 'java/io/DataOutputStream', 'writeShort', '(I)V')],
		'return'
	])
	a_code = code_attribute.assemble([
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
	m = make_method(['public'], icpx_utf8(xcp, 'a'), icpx_utf8(xcp, '(Lme;)V'))

	code = instructions.make(0, [
		'aload_1',
		'aload_0',
		['invokevirtual', icpx_m(xcp, 'me', 'onHungerUpdate', '(Lcom/thebluetropics/crabpack/HungerUpdatePacket;)V')],
		'return'
	])
	a_code = code_attribute.assemble([
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
	m = make_method(['public'], icpx_utf8(xcp, 'a'), icpx_utf8(xcp, '()I'))

	code = instructions.make(0, [
		'iconst_4',
		'ireturn'
	])
	a_code = code_attribute.assemble([
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
