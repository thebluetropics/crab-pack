import os
import mod

from operator import eq
from mod.bytecode import (
	class_file,
	code_attribute,
	instructions,
	utf8
)

def apply_client():
	cf = class_file.create_template()

	cp_sz = 38
	cp = [
		[1, b"\x01", len("com/thebluetropics/crabpack/UpdateHungerPacket").to_bytes(2), utf8.encode("com/thebluetropics/crabpack/UpdateHungerPacket")],
		[2, b"\x07", (1).to_bytes(2)],
		[3, b"\x01", len("ki").to_bytes(2), utf8.encode("ki")],
		[4, b"\x07", (3).to_bytes(2)],
		[5, b"\x01", len("hunger").to_bytes(2), utf8.encode("hunger")],
		[6, b"\x01", len("I").to_bytes(2), utf8.encode("I")],
		[7, b"\x0c", (5).to_bytes(2) + (6).to_bytes(2)],
		[8, b"\x09", (2).to_bytes(2) + (7).to_bytes(2)],
		[9, b"\x01", len("<init>").to_bytes(2), utf8.encode("<init>")],
		[10, b"\x01", len("(I)V").to_bytes(2), utf8.encode("(I)V")],
		[11, b"\x01", len("()V").to_bytes(2), utf8.encode("()V")],
		[12, b"\x0c", (9).to_bytes(2) + (11).to_bytes(2)],
		[13, b"\x0a", (4).to_bytes(2) + (12).to_bytes(2)],
		[14, b"\x01", len("Code").to_bytes(2), utf8.encode("Code")],
		[15, b"\x01", len("read").to_bytes(2), utf8.encode("read")],
		[16, b"\x01", len("(Ljava/io/DataInputStream;)V").to_bytes(2), utf8.encode("(Ljava/io/DataInputStream;)V")],
		[17, b"\x01", len("DataInputStream").to_bytes(2), utf8.encode("DataInputStream")],
		[18, b"\x07", (17).to_bytes(2)],
		[19, b"\x01", len("readShort").to_bytes(2), utf8.encode("readShort")],
		[20, b"\x01", len("()S").to_bytes(2), utf8.encode("()S")],
		[21, b"\x0c", (19).to_bytes(2) + (20).to_bytes(2)],
		[22, b"\x0a", (18).to_bytes(2) + (21).to_bytes(2)],
		[23, b"\x01", len("write").to_bytes(2), utf8.encode("write")],
		[24, b"\x01", len("(Ljava/io/DataOutputStream;)V").to_bytes(2), utf8.encode("(Ljava/io/DataOutputStream;)V")],
		[25, b"\x01", len("DataOutputStream").to_bytes(2), utf8.encode("DataOutputStream")],
		[26, b"\x07", (25).to_bytes(2)],
		[27, b"\x01", len("writeShort").to_bytes(2), utf8.encode("writeShort")],
		[28, b"\x0c", (27).to_bytes(2) + (10).to_bytes(2)],
		[29, b"\x0a", (26).to_bytes(2) + (28).to_bytes(2)],
		[30, b"\x01", len("apply").to_bytes(2), utf8.encode("apply")],
		[31, b"\x01", len("(Lti;)V").to_bytes(2), utf8.encode("(Lti;)V")],
		[32, b"\x01", len("ti").to_bytes(2), utf8.encode("ti")],
		[33, b"\x07", (32).to_bytes(2)],
		[34, b"\x01", len("a").to_bytes(2), utf8.encode("a")],
		[35, b"\x01", len("(Leu;)V").to_bytes(2), utf8.encode("(Leu;)V")],
		[36, b"\x0c", (34).to_bytes(2) + (35).to_bytes(2)],
		[37, b"\x0a", (33).to_bytes(2) + (36).to_bytes(2)],
		[38, b"\x01", len("size").to_bytes(2), utf8.encode("size")],
		[39, b"\x01", len("()I").to_bytes(2), utf8.encode("()I")]
	]
	cf[0x03], cf[0x04] = (cp_sz.to_bytes(2), cp)

	cf[0x05] = (0x0001.__or__(0x0020)).to_bytes(2)
	cf[0x06] = (2).to_bytes(2)
	cf[0x07] = (4).to_bytes(2)

	f_count = 1
	fields = [
		[(0x0001).to_bytes(2), (5).to_bytes(2), (6).to_bytes(2), (0).to_bytes(2), []]
	]
	cf[0x0a], cf[0x0b] = (f_count.to_bytes(2), fields)

	m_count = 5
	methods = [
		_make_constructor_1c(),
		_make_read_m_1c(),
		_make_write_m_1c(),
		_make_m_apply_1c(),
		_make_m_size_1c()
	]
	cf[0x0c], cf[0x0d] = (m_count.to_bytes(2), methods)

	if not os.path.exists("stage/client/com/thebluetropics/crabpack"):
		os.makedirs("stage/client/com/thebluetropics/crabpack", exist_ok=True)

	with open(mod.config.path("stage/client/com/thebluetropics/crabpack/UpdateHungerPacket.class"), "wb") as file:
		file.write(class_file.make(cf))

def _make_constructor_1c():
	m = [None] * 5

	m[0x00] = (0x0001).to_bytes(2)
	m[0x01] = (9).to_bytes(2)
	m[0x02] = (10).to_bytes(2)

	code = instructions.make(0, [
		'aload_0', ['invokespecial', 13],
		'aload_0', ['iload_1'], ['putfield', 8],
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

	a = [(14).to_bytes(2), len(a_code).to_bytes(4), a_code]

	m[0x03] = (1).to_bytes(2)
	m[0x04] = [a]

	return m

def _make_read_m_1c():
	m = [None] * 5

	m[0x00] = (0x0001).to_bytes(2)
	m[0x01] = (15).to_bytes(2)
	m[0x02] = (16).to_bytes(2)

	code = instructions.make(0, [
		'aload_0',
		'aload_1', ['invokevirtual', 22],
		['putfield', 8],
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

	a = [(14).to_bytes(2), len(a_code).to_bytes(4), a_code]

	m[0x03] = (1).to_bytes(2)
	m[0x04] = [a]

	return m

def _make_write_m_1c():
	m = [None] * 5

	m[0x00] = (0x0001).to_bytes(2)
	m[0x01] = (23).to_bytes(2)
	m[0x02] = (24).to_bytes(2)

	code = instructions.make(0, [
		'aload_1',
		'aload_0', ['getfield', 8],
		['invokevirtual', 29],
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

	a = [(14).to_bytes(2), len(a_code).to_bytes(4), a_code]

	m[0x03] = (1).to_bytes(2)
	m[0x04] = [a]

	return m

def _make_m_apply_1c():
	m = [None] * 5

	m[0x00] = (0x0001).to_bytes(2)
	m[0x01] = (30).to_bytes(2)
	m[0x02] = (31).to_bytes(2)

	code = instructions.make(0, [
		'aload_1',
		'aload_0',
		['invokevirtual', 37],
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

	a = [(14).to_bytes(2), len(a_code).to_bytes(4), a_code]

	m[0x03] = (1).to_bytes(2)
	m[0x04] = [a]

	return m

def _make_m_size_1c():
	m = [None] * 5

	m[0x00] = (0x0001).to_bytes(2)
	m[0x01] = (38).to_bytes(2)
	m[0x02] = (39).to_bytes(2)

	code = instructions.make(0, [
		'iconst_2',
		'ireturn'
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

	a = [(14).to_bytes(2), len(a_code).to_bytes(4), a_code]

	m[0x03] = (1).to_bytes(2)
	m[0x04] = [a]

	return m

def apply_server():
	pass
