import struct

from sys import exit, stderr
from operator import eq
from .cp import *

def a_code_load(buf):
	a_code = [None] * 8

	a_code[0x00] = buf[0:2]
	a_code[0x01] = buf[2:4]

	a_code[0x02] = buf[4:8]
	code_length = int.from_bytes(a_code[0x02])

	a_code[0x03] = buf[8:8 + code_length]
	i = 8 + code_length

	a_code[0x04] = buf[i:i + 2]
	exception_table_length = int.from_bytes(a_code[0x04])
	i = i + 2

	a_code[0x05] = []
	exception_table = a_code[0x05]

	for _ in range(exception_table_length):
		exception_table.append([
			buf[i:i + 2],
			buf[i + 2:i + 4],
			buf[i + 4:i + 6],
			buf[i + 6:i + 8]
		])
		i = i + 8

	a_code[0x06] = buf[i:i + 2]
	a_count = int.from_bytes(a_code[0x06])
	i = i + 2

	a_code[0x07] = []
	attributes = a_code[0x07]

	for _ in range(a_count):
		a = [
			buf[i:i + 2],
			buf[i + 2:i + 6],
			None
		]
		sz = int.from_bytes(a[0x01])
		a[0x02] = buf[i + 6:i + 6 + sz]
		attributes.append(a)
		i = i + 6 + sz

	return a_code

def a_code_assemble(a_code):
	return b''.join([
		a_code[0x00], a_code[0x01],
		a_code[0x02], a_code[0x03],
		a_code[0x04],
		*[b''.join(entry) for entry in a_code[0x05]],
		a_code[0x06],
		*[b''.join(a) for a in a_code[0x07]]
	])

def load_code(cp_cache, buf):
	code = []
	i = 0

	while i < len(buf):
		if eq(buf[i].to_bytes(1), b'\x00'):
			code.append('nop')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x01'):
			code.append('aconst_null')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x02'):
			code.append('iconst_m1')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x03'):
			code.append('iconst_0')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x04'):
			code.append('iconst_1')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x05'):
			code.append('iconst_2')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x06'):
			code.append('iconst_3')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x07'):
			code.append('iconst_4')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x08'):
			code.append('iconst_5')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x09'):
			code.append('lconst_0')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x0a'):
			code.append('lconst_1')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x0b'):
			code.append('fconst_0')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x0c'):
			code.append('fconst_1')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x0d'):
			code.append('fconst_2')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x0e'):
			code.append('dconst_0')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x0f'):
			code.append('dconst_1')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x1a'):
			code.append('iload_0')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x1b'):
			code.append('iload_1')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x1c'):
			code.append('iload_2')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x1d'):
			code.append('iload_3')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x1e'):
			code.append('lload_0')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x1f'):
			code.append('lload_1')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x20'):
			code.append('lload_2')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x21'):
			code.append('lload_3')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x22'):
			code.append('fload_0')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x23'):
			code.append('fload_1')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x24'):
			code.append('fload_2')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x25'):
			code.append('fload_3')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x26'):
			code.append('dload_0')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x27'):
			code.append('dload_1')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x28'):
			code.append('dload_2')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x29'):
			code.append('dload_3')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x2a'):
			code.append('aload_0')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x2b'):
			code.append('aload_1')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x2c'):
			code.append('aload_2')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x2d'):
			code.append('aload_3')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x2e'):
			code.append('iaload')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x2f'):
			code.append('laload')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x30'):
			code.append('faload')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x31'):
			code.append('daload')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x32'):
			code.append('aaload')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x33'):
			code.append('baload')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x34'):
			code.append('caload')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x35'):
			code.append('saload')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x3b'):
			code.append('istore_0')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x3c'):
			code.append('istore_1')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x3d'):
			code.append('istore_2')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x3e'):
			code.append('istore_3')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x3f'):
			code.append('lstore_0')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x40'):
			code.append('lstore_1')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x41'):
			code.append('lstore_2')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x42'):
			code.append('lstore_3')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x43'):
			code.append('fstore_0')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x44'):
			code.append('fstore_1')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x45'):
			code.append('fstore_2')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x46'):
			code.append('fstore_3')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x47'):
			code.append('dstore_0')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x48'):
			code.append('dstore_1')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x49'):
			code.append('dstore_2')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x4a'):
			code.append('dstore_3')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x4b'):
			code.append('astore_0')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x4c'):
			code.append('astore_1')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x4d'):
			code.append('astore_2')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x4e'):
			code.append('astore_3')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x4f'):
			code.append('iastore')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x50'):
			code.append('lastore')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x51'):
			code.append('fastore')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x52'):
			code.append('dastore')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x53'):
			code.append('aastore')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x54'):
			code.append('bastore')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x55'):
			code.append('castore')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x56'):
			code.append('sastore')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x57'):
			code.append('pop')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x58'):
			code.append('pop2')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x59'):
			code.append('dup')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x5a'):
			code.append('dup_x1')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x5b'):
			code.append('dup_x2')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x5c'):
			code.append('dup2')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x5d'):
			code.append('dup2_x1')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x5e'):
			code.append('dup2_x2')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x5f'):
			code.append('swap')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x60'):
			code.append('iadd')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x61'):
			code.append('ladd')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x62'):
			code.append('fadd')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x63'):
			code.append('dadd')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x64'):
			code.append('isub')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x65'):
			code.append('lsub')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x66'):
			code.append('fsub')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x67'):
			code.append('dsub')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x68'):
			code.append('imul')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x69'):
			code.append('lmul')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x6a'):
			code.append('fmul')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x6b'):
			code.append('dmul')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x6c'):
			code.append('idiv')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x6d'):
			code.append('ldiv')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x6e'):
			code.append('fdiv')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x6f'):
			code.append('ddiv')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x70'):
			code.append('irem')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x71'):
			code.append('lrem')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x72'):
			code.append('frem')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x73'):
			code.append('drem')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x74'):
			code.append('ineg')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x75'):
			code.append('lneg')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x76'):
			code.append('fneg')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x77'):
			code.append('dneg')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x78'):
			code.append('ishl')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x79'):
			code.append('lshl')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x7a'):
			code.append('ishr')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x7b'):
			code.append('lshr')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x7c'):
			code.append('iushr')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x7d'):
			code.append('lushr')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x7e'):
			code.append('iand')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x7f'):
			code.append('land')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x80'):
			code.append('ior')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x81'):
			code.append('lor')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x82'):
			code.append('ixor')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x83'):
			code.append('lxor')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x85'):
			code.append('i2l')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x86'):
			code.append('i2f')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x87'):
			code.append('i2d')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x88'):
			code.append('l2i')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x89'):
			code.append('l2f')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x8a'):
			code.append('l2d')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x8b'):
			code.append('f2i')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x8c'):
			code.append('f2l')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x8d'):
			code.append('f2d')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x8e'):
			code.append('d2i')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x8f'):
			code.append('d2l')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x90'):
			code.append('d2f')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x91'):
			code.append('i2b')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x92'):
			code.append('i2c')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x93'):
			code.append('i2s')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x94'):
			code.append('lcmp')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x95'):
			code.append('fcmpl')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x96'):
			code.append('fcmpg')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x97'):
			code.append('dcmpl')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x98'):
			code.append('dcmpg')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\xac'):
			code.append('ireturn')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\xad'):
			code.append('lreturn')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\xae'):
			code.append('freturn')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\xaf'):
			code.append('dreturn')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\xb0'):
			code.append('areturn')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\xb1'):
			code.append('return')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\xbe'):
			code.append('arraylength')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\xbf'):
			code.append('athrow')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\xc2'):
			code.append('monitorenter')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\xc3'):
			code.append('monitorexit')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\xca'):
			code.append('breakpoint')
			i = i + 1
			continue

		if eq(buf[i].to_bytes(1), b'\x10'):
			code.append(['bipush', int.from_bytes(buf[i + 1:i + 2], signed=True)])
			i = i + 2
			continue

		if eq(buf[i].to_bytes(1), b'\x11'):
			code.append(['sipush', int.from_bytes(buf[i + 1:i + 3], signed=True)])
			i = i + 3
			continue

		if eq(buf[i].to_bytes(1), b'\x15'):
			code.append(['iload', buf[i + 1]])
			i = i + 2
			continue

		if eq(buf[i].to_bytes(1), b'\x16'):
			code.append(['lload', buf[i + 1]])
			i = i + 2
			continue

		if eq(buf[i].to_bytes(1), b'\x17'):
			code.append(['fload', buf[i + 1]])
			i = i + 2
			continue

		if eq(buf[i].to_bytes(1), b'\x18'):
			code.append(['dload', buf[i + 1]])
			i = i + 2
			continue

		if eq(buf[i].to_bytes(1), b'\x19'):
			code.append(['aload', buf[i + 1]])
			i = i + 2
			continue

		if eq(buf[i].to_bytes(1), b'\x36'):
			code.append(['istore', buf[i + 1]])
			i = i + 2
			continue

		if eq(buf[i].to_bytes(1), b'\x37'):
			code.append(['lstore', buf[i + 1]])
			i = i + 2
			continue

		if eq(buf[i].to_bytes(1), b'\x38'):
			code.append(['fstore', buf[i + 1]])
			i = i + 2
			continue

		if eq(buf[i].to_bytes(1), b'\x39'):
			code.append(['dstore', buf[i + 1]])
			i = i + 2
			continue

		if eq(buf[i].to_bytes(1), b'\x3a'):
			code.append(['astore', buf[i + 1]])
			i = i + 2
			continue

		if eq(buf[i].to_bytes(1), b'\x84'):
			code.append([
				'iinc',
				int.from_bytes(buf[i + 1:i + 2], signed=True),
				int.from_bytes(buf[i + 2:i + 3], signed=True)
			])
			i = i + 3
			continue

		if eq(buf[i].to_bytes(1), b'\xa9'):
			code.append(['ret', buf[i + 1]])
			i = i + 2
			continue

		if eq(buf[i].to_bytes(1), b'\x99'):
			code.append(['ifeq', int.from_bytes(buf[i + 1:i + 3], signed=True)])
			i = i + 3
			continue

		if eq(buf[i].to_bytes(1), b'\x9a'):
			code.append(['ifne', int.from_bytes(buf[i + 1:i + 3], signed=True)])
			i = i + 3
			continue

		if eq(buf[i].to_bytes(1), b'\x9b'):
			code.append(['iflt', int.from_bytes(buf[i + 1:i + 3], signed=True)])
			i = i + 3
			continue

		if eq(buf[i].to_bytes(1), b'\x9c'):
			code.append(['ifge', int.from_bytes(buf[i + 1:i + 3], signed=True)])
			i = i + 3
			continue

		if eq(buf[i].to_bytes(1), b'\x9d'):
			code.append(['ifgt', int.from_bytes(buf[i + 1:i + 3], signed=True)])
			i = i + 3
			continue

		if eq(buf[i].to_bytes(1), b'\x9e'):
			code.append(['ifle', int.from_bytes(buf[i + 1:i + 3], signed=True)])
			i = i + 3
			continue

		if eq(buf[i].to_bytes(1), b'\x9f'):
			code.append(['if_icmpeq', int.from_bytes(buf[i + 1:i + 3], signed=True)])
			i = i + 3
			continue

		if eq(buf[i].to_bytes(1), b'\xa0'):
			code.append(['if_icmpne', int.from_bytes(buf[i + 1:i + 3], signed=True)])
			i = i + 3
			continue

		if eq(buf[i].to_bytes(1), b'\xa1'):
			code.append(['if_icmplt', int.from_bytes(buf[i + 1:i + 3], signed=True)])
			i = i + 3
			continue

		if eq(buf[i].to_bytes(1), b'\xa2'):
			code.append(['if_icmpge', int.from_bytes(buf[i + 1:i + 3], signed=True)])
			i = i + 3
			continue

		if eq(buf[i].to_bytes(1), b'\xa3'):
			code.append(['if_icmpgt', int.from_bytes(buf[i + 1:i + 3], signed=True)])
			i = i + 3
			continue

		if eq(buf[i].to_bytes(1), b'\xa4'):
			code.append(['if_icmple', int.from_bytes(buf[i + 1:i + 3], signed=True)])
			i = i + 3
			continue

		if eq(buf[i].to_bytes(1), b'\xa5'):
			code.append(['if_acmpeq', int.from_bytes(buf[i + 1:i + 3], signed=True)])
			i = i + 3
			continue

		if eq(buf[i].to_bytes(1), b'\xa6'):
			code.append(['if_acmpne', int.from_bytes(buf[i + 1:i + 3], signed=True)])
			i = i + 3
			continue

		if eq(buf[i].to_bytes(1), b'\xa7'):
			code.append(['goto', int.from_bytes(buf[i + 1:i + 3], signed=True)])
			i = i + 3
			continue

		if eq(buf[i].to_bytes(1), b'\xc6'):
			code.append(['ifnull', int.from_bytes(buf[i + 1:i + 3], signed=True)])
			i = i + 3
			continue

		if eq(buf[i].to_bytes(1), b'\xc7'):
			code.append(['ifnonnull', int.from_bytes(buf[i + 1:i + 3], signed=True)])
			i = i + 3
			continue

		if eq(buf[i].to_bytes(1), b'\xa8'):
			code.append(['jsr', int.from_bytes(buf[i + 1:i + 3], signed=True)])
			i = i + 3
			continue

		if eq(buf[i].to_bytes(1), b'\xc8'):
			code.append(['goto_w', int.from_bytes(buf[i + 1:i + 5], signed=True)])
			i = i + 5
			continue

		if eq(buf[i].to_bytes(1), b'\xc9'):
			code.append(['jsr_w', int.from_bytes(buf[i + 1:i + 5], signed=True)])
			i = i + 5
			continue

		if eq(buf[i].to_bytes(1), b'\x12'):
			j = buf[i + 1]
			entry = cp_get_entry(cp_cache, j)

			if eq(entry[1], b'\x08'):
				code.append(['ldc.string', cp_get_string(cp_cache, j)])

			if eq(entry[1], b'\x07'):
				code.append(['ldc.class', cp_get_class(cp_cache, j)])

			if eq(entry[1], b'\x03'):
				code.append(['ldc.i32', cp_get_i32(cp_cache, j)])

			if eq(entry[1], b'\x04'):
				code.append(['ldc.f32', cp_get_f32(cp_cache, j)])

			if eq(entry[1], b'\x0f'):
				print('Err: unknown.', file=stderr)
				exit(1)

			if eq(entry[1], b'\x10'):
				print('Err: unknown.', file=stderr)
				exit(1)

			i = i + 2
			continue

		if eq(buf[i].to_bytes(1), b'\x13'):
			j = int.from_bytes(buf[i + 1:i + 3])
			entry = cp_get_entry(cp_cache, j)

			if eq(entry[1], b'\x08'):
				code.append(['ldc_w.string', cp_get_string(cp_cache, j)])

			if eq(entry[1], b'\x07'):
				code.append(['ldc_w.class', cp_get_class(cp_cache, j)])

			if eq(entry[1], b'\x03'):
				code.append(['ldc_w.i32', cp_get_i32(cp_cache, j)])

			if eq(entry[1], b'\x04'):
				code.append(['ldc_w.f32', cp_get_f32(cp_cache, j)])

			if eq(entry[1], b'\x0f'):
				print('Err: unknown.', file=stderr)
				exit(1)

			if eq(entry[1], b'\x10'):
				print('Err: unknown.', file=stderr)
				exit(1)

			i = i + 3
			continue

		if eq(buf[i].to_bytes(1), b'\x14'):
			j = int.from_bytes(buf[i + 1:i + 3])
			entry = cp_get_entry(cp_cache, j)

			if eq(entry[1], b'\x05'):
				code.append(['ldc2_w.i64', cp_get_i64(cp_cache, j)])

			if eq(entry[1], b'\x06'):
				code.append(['ldc2_w.f64', cp_get_f64(cp_cache, j)])

			i = i + 3
			continue

		if eq(buf[i].to_bytes(1), b'\xb2'):
			code.append(['getstatic', *cp_get_field_reference(cp_cache, int.from_bytes(buf[i + 1:i + 3]))])
			i = i + 3
			continue

		if eq(buf[i].to_bytes(1), b'\xb3'):
			code.append(['putstatic', *cp_get_field_reference(cp_cache, int.from_bytes(buf[i + 1:i + 3]))])
			i = i + 3
			continue

		if eq(buf[i].to_bytes(1), b'\xb4'):
			code.append(['getfield', *cp_get_field_reference(cp_cache, int.from_bytes(buf[i + 1:i + 3]))])
			i = i + 3
			continue

		if eq(buf[i].to_bytes(1), b'\xb5'):
			code.append(['putfield', *cp_get_field_reference(cp_cache, int.from_bytes(buf[i + 1:i + 3]))])
			i = i + 3
			continue

		if eq(buf[i].to_bytes(1), b'\xbb'):
			code.append(['new', cp_get_class(cp_cache, int.from_bytes(buf[i + 1:i + 3]))])
			i = i + 3
			continue

		if eq(buf[i].to_bytes(1), b'\xbc'):
			code.append(['newarray', buf[i + 1]])
			i = i + 2
			continue

		if eq(buf[i].to_bytes(1), b'\xbd'):
			code.append(['anewarray', cp_get_class(cp_cache, int.from_bytes(buf[i + 1:i + 3]))])
			i = i + 3
			continue

		if eq(buf[i].to_bytes(1), b'\xc0'):
			code.append(['checkcast', cp_get_class(cp_cache, int.from_bytes(buf[i + 1:i + 3]))])
			i = i + 3
			continue

		if eq(buf[i].to_bytes(1), b'\xc1'):
			code.append(['instanceof', cp_get_class(cp_cache, int.from_bytes(buf[i + 1:i + 3]))])
			i = i + 3
			continue

		if eq(buf[i].to_bytes(1), b'\xb6'):
			code.append(['invokevirtual', *cp_get_method_reference(cp_cache, int.from_bytes(buf[i + 1:i + 3]))])
			i = i + 3
			continue

		if eq(buf[i].to_bytes(1), b'\xb7'):
			code.append(['invokespecial', *cp_get_method_reference(cp_cache, int.from_bytes(buf[i + 1:i + 3]))])
			i = i + 3
			continue

		if eq(buf[i].to_bytes(1), b'\xb8'):
			code.append(['invokestatic', *cp_get_method_reference(cp_cache, int.from_bytes(buf[i + 1:i + 3]))])
			i = i + 3
			continue

		if eq(buf[i].to_bytes(1), b'\xb9'):
			code.append(['invokeinterface', *cp_get_interface_method_reference(cp_cache, int.from_bytes(buf[i + 1:i + 3])), buf[i + 3]])
			i = i + 5
			continue

		print('Err: unknown instruction -> ', buf[i], file=stderr)
		exit(1)

	return code

def assemble_code(cf, cp_cache, select, pc_begin, code):
	stage = []
	target_table = {}
	i = pc_begin

	for ins in code:
		if isinstance(ins, str) and ins.__eq__('nop'):
			stage.append(b'\x00')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('aconst_null'):
			stage.append(b'\x01')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('iconst_m1'):
			stage.append(b'\x02')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('iconst_0'):
			stage.append(b'\x03')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('iconst_1'):
			stage.append(b'\x04')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('iconst_2'):
			stage.append(b'\x05')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('iconst_3'):
			stage.append(b'\x06')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('iconst_4'):
			stage.append(b'\x07')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('iconst_5'):
			stage.append(b'\x08')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('lconst_0'):
			stage.append(b'\x09')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('lconst_1'):
			stage.append(b'\x0a')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('fconst_0'):
			stage.append(b'\x0b')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('fconst_1'):
			stage.append(b'\x0c')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('fconst_2'):
			stage.append(b'\x0d')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('dconst_0'):
			stage.append(b'\x0e')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('dconst_1'):
			stage.append(b'\x0f')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('iload_0'):
			stage.append(b'\x1a')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('iload_1'):
			stage.append(b'\x1b')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('iload_2'):
			stage.append(b'\x1c')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('iload_3'):
			stage.append(b'\x1d')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('lload_0'):
			stage.append(b'\x1e')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('lload_1'):
			stage.append(b'\x1f')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('lload_2'):
			stage.append(b'\x20')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('lload_3'):
			stage.append(b'\x21')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('fload_0'):
			stage.append(b'\x22')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('fload_1'):
			stage.append(b'\x23')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('fload_2'):
			stage.append(b'\x24')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('fload_3'):
			stage.append(b'\x25')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('dload_0'):
			stage.append(b'\x26')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('dload_1'):
			stage.append(b'\x27')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('dload_2'):
			stage.append(b'\x28')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('dload_3'):
			stage.append(b'\x29')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('aload_0'):
			stage.append(b'\x2a')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('aload_1'):
			stage.append(b'\x2b')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('aload_2'):
			stage.append(b'\x2c')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('aload_3'):
			stage.append(b'\x2d')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('iaload'):
			stage.append(b'\x2e')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('laload'):
			stage.append(b'\x2f')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('faload'):
			stage.append(b'\x30')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('daload'):
			stage.append(b'\x31')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('aaload'):
			stage.append(b'\x32')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('baload'):
			stage.append(b'\x33')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('caload'):
			stage.append(b'\x34')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('saload'):
			stage.append(b'\x35')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('istore_0'):
			stage.append(b'\x3b')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('istore_1'):
			stage.append(b'\x3c')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('istore_2'):
			stage.append(b'\x3d')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('istore_3'):
			stage.append(b'\x3e')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('lstore_0'):
			stage.append(b'\x3f')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('lstore_1'):
			stage.append(b'\x40')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('lstore_2'):
			stage.append(b'\x41')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('lstore_3'):
			stage.append(b'\x42')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('fstore_0'):
			stage.append(b'\x43')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('fstore_1'):
			stage.append(b'\x44')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('fstore_2'):
			stage.append(b'\x45')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('fstore_3'):
			stage.append(b'\x46')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('dstore_0'):
			stage.append(b'\x47')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('dstore_1'):
			stage.append(b'\x48')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('dstore_2'):
			stage.append(b'\x49')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('dstore_3'):
			stage.append(b'\x4a')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('astore_0'):
			stage.append(b'\x4b')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('astore_1'):
			stage.append(b'\x4c')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('astore_2'):
			stage.append(b'\x4d')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('astore_3'):
			stage.append(b'\x4e')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('iastore'):
			stage.append(b'\x4f')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('lastore'):
			stage.append(b'\x50')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('fastore'):
			stage.append(b'\x51')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('dastore'):
			stage.append(b'\x52')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('aastore'):
			stage.append(b'\x53')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('bastore'):
			stage.append(b'\x54')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('castore'):
			stage.append(b'\x55')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('sastore'):
			stage.append(b'\x56')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('pop'):
			stage.append(b'\x57')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('pop2'):
			stage.append(b'\x58')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('dup'):
			stage.append(b'\x59')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('dup_x1'):
			stage.append(b'\x5a')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('dup_x2'):
			stage.append(b'\x5b')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('dup2'):
			stage.append(b'\x5c')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('dup2_x1'):
			stage.append(b'\x5d')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('dup2_x2'):
			stage.append(b'\x5e')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('swap'):
			stage.append(b'\x5f')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('iadd'):
			stage.append(b'\x60')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('ladd'):
			stage.append(b'\x61')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('fadd'):
			stage.append(b'\x62')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('dadd'):
			stage.append(b'\x63')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('isub'):
			stage.append(b'\x64')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('lsub'):
			stage.append(b'\x65')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('fsub'):
			stage.append(b'\x66')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('dsub'):
			stage.append(b'\x67')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('imul'):
			stage.append(b'\x68')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('lmul'):
			stage.append(b'\x69')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('fmul'):
			stage.append(b'\x6a')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('dmul'):
			stage.append(b'\x6b')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('idiv'):
			stage.append(b'\x6c')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('ldiv'):
			stage.append(b'\x6d')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('fdiv'):
			stage.append(b'\x6e')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('ddiv'):
			stage.append(b'\x6f')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('irem'):
			stage.append(b'\x70')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('lrem'):
			stage.append(b'\x71')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('frem'):
			stage.append(b'\x72')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('drem'):
			stage.append(b'\x73')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('ineg'):
			stage.append(b'\x74')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('lneg'):
			stage.append(b'\x75')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('fneg'):
			stage.append(b'\x76')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('dneg'):
			stage.append(b'\x77')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('ishl'):
			stage.append(b'\x78')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('lshl'):
			stage.append(b'\x79')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('ishr'):
			stage.append(b'\x7a')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('lshr'):
			stage.append(b'\x7b')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('iushr'):
			stage.append(b'\x7c')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('lushr'):
			stage.append(b'\x7d')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('iand'):
			stage.append(b'\x7e')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('land'):
			stage.append(b'\x7f')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('ior'):
			stage.append(b'\x80')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('lor'):
			stage.append(b'\x81')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('ixor'):
			stage.append(b'\x82')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('lxor'):
			stage.append(b'\x83')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('i2l'):
			stage.append(b'\x85')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('i2f'):
			stage.append(b'\x86')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('i2d'):
			stage.append(b'\x87')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('l2i'):
			stage.append(b'\x88')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('l2f'):
			stage.append(b'\x89')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('l2d'):
			stage.append(b'\x8a')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('f2i'):
			stage.append(b'\x8b')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('f2l'):
			stage.append(b'\x8c')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('f2d'):
			stage.append(b'\x8d')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('d2i'):
			stage.append(b'\x8e')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('d2l'):
			stage.append(b'\x8f')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('d2f'):
			stage.append(b'\x90')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('i2b'):
			stage.append(b'\x91')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('i2c'):
			stage.append(b'\x92')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('i2s'):
			stage.append(b'\x93')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('lcmp'):
			stage.append(b'\x94')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('fcmpl'):
			stage.append(b'\x95')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('fcmpg'):
			stage.append(b'\x96')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('dcmpl'):
			stage.append(b'\x97')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('dcmpg'):
			stage.append(b'\x98')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('ireturn'):
			stage.append(b'\xac')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('lreturn'):
			stage.append(b'\xad')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('freturn'):
			stage.append(b'\xae')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('dreturn'):
			stage.append(b'\xaf')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('areturn'):
			stage.append(b'\xb0')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('return'):
			stage.append(b'\xb1')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('arraylength'):
			stage.append(b'\xbe')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('athrow'):
			stage.append(b'\xbf')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('monitorenter'):
			stage.append(b'\xc2')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('monitorexit'):
			stage.append(b'\xc3')
			i = i + 1
			continue

		if isinstance(ins, str) and ins.__eq__('breakpoint'):
			stage.append(b'\xca')
			i = i + 1
			continue

		if isinstance(ins, list) and ins[0].__eq__('bipush'):
			stage.append(b'\x10' + ins[1].to_bytes(1))
			i = i + 2
			continue

		if isinstance(ins, list) and ins[0].__eq__('sipush'):
			stage.append(b'\x11' + ins[1].to_bytes(2))
			i = i + 3
			continue

		if isinstance(ins, list) and ins[0].__eq__('iload'):
			stage.append(b'\x15' + ins[1].to_bytes(1))
			i = i + 2
			continue

		if isinstance(ins, list) and ins[0].__eq__('lload'):
			stage.append(b'\x16' + ins[1].to_bytes(1))
			i = i + 2
			continue

		if isinstance(ins, list) and ins[0].__eq__('fload'):
			stage.append(b'\x17' + ins[1].to_bytes(1))
			i = i + 2
			continue

		if isinstance(ins, list) and ins[0].__eq__('dload'):
			stage.append(b'\x18' + ins[1].to_bytes(1))
			i = i + 2
			continue

		if isinstance(ins, list) and ins[0].__eq__('aload'):
			stage.append(b'\x19' + ins[1].to_bytes(1))
			i = i + 2
			continue

		if isinstance(ins, list) and ins[0].__eq__('istore'):
			stage.append(b'\x36' + ins[1].to_bytes(1))
			i = i + 2
			continue

		if isinstance(ins, list) and ins[0].__eq__('lstore'):
			stage.append(b'\x37' + ins[1].to_bytes(1))
			i = i + 2
			continue

		if isinstance(ins, list) and ins[0].__eq__('fstore'):
			stage.append(b'\x38' + ins[1].to_bytes(1))
			i = i + 2
			continue

		if isinstance(ins, list) and ins[0].__eq__('dstore'):
			stage.append(b'\x39' + ins[1].to_bytes(1))
			i = i + 2
			continue

		if isinstance(ins, list) and ins[0].__eq__('astore'):
			stage.append(b'\x3a' + ins[1].to_bytes(1))
			i = i + 2
			continue

		if isinstance(ins, list) and ins[0].__eq__('iinc'):
			stage.append(b'\x84' + ins[1].to_bytes(1) + ins[2].to_bytes(1))
			i = i + 3
			continue

		if isinstance(ins, list) and ins[0].__eq__('ret'):
			stage.append(b'\xa9' + ins[1].to_bytes(1))
			i = i + 2
			continue

		if isinstance(ins, list) and ins[0].__eq__('ifeq'):
			if type(ins[1]) is str:
				stage.append(ins)
			else:
				stage.append(b'\x99' + ins[1].to_bytes(2, signed=True))
			i = i + 3
			continue

		if isinstance(ins, list) and ins[0].__eq__('ifne'):
			if type(ins[1]) is str:
				stage.append(ins)
			else:
				stage.append(b'\x9a' + ins[1].to_bytes(2, signed=True))
			i = i + 3
			continue

		if isinstance(ins, list) and ins[0].__eq__('iflt'):
			if type(ins[1]) is str:
				stage.append(ins)
			else:
				stage.append(b'\x9b' + ins[1].to_bytes(2, signed=True))
			i = i + 3
			continue

		if isinstance(ins, list) and ins[0].__eq__('ifge'):
			if type(ins[1]) is str:
				stage.append(ins)
			else:
				stage.append(b'\x9c' + ins[1].to_bytes(2, signed=True))
			i = i + 3
			continue

		if isinstance(ins, list) and ins[0].__eq__('ifgt'):
			if type(ins[1]) is str:
				stage.append(ins)
			else:
				stage.append(b'\x9d' + ins[1].to_bytes(2, signed=True))
			i = i + 3
			continue

		if isinstance(ins, list) and ins[0].__eq__('ifle'):
			if type(ins[1]) is str:
				stage.append(ins)
			else:
				stage.append(b'\x9e' + ins[1].to_bytes(2, signed=True))
			i = i + 3
			continue

		if isinstance(ins, list) and ins[0].__eq__('if_icmpeq'):
			if type(ins[1]) is str:
				stage.append(ins)
			else:
				stage.append(b'\x9f' + ins[1].to_bytes(2, signed=True))
			i = i + 3
			continue

		if isinstance(ins, list) and ins[0].__eq__('if_icmpne'):
			if type(ins[1]) is str:
				stage.append(ins)
			else:
				stage.append(b'\xa0' + ins[1].to_bytes(2, signed=True))
			i = i + 3
			continue

		if isinstance(ins, list) and ins[0].__eq__('if_icmplt'):
			if type(ins[1]) is str:
				stage.append(ins)
			else:
				stage.append(b'\xa1' + ins[1].to_bytes(2, signed=True))
			i = i + 3
			continue

		if isinstance(ins, list) and ins[0].__eq__('if_icmpge'):
			if type(ins[1]) is str:
				stage.append(ins)
			else:
				stage.append(b'\xa2' + ins[1].to_bytes(2, signed=True))
			i = i + 3
			continue

		if isinstance(ins, list) and ins[0].__eq__('if_icmpgt'):
			if type(ins[1]) is str:
				stage.append(ins)
			else:
				stage.append(b'\xa3' + ins[1].to_bytes(2, signed=True))
			i = i + 3
			continue

		if isinstance(ins, list) and ins[0].__eq__('if_icmple'):
			if type(ins[1]) is str:
				stage.append(ins)
			else:
				stage.append(b'\xa4' + ins[1].to_bytes(2, signed=True))
			i = i + 3
			continue

		if isinstance(ins, list) and ins[0].__eq__('if_acmpeq'):
			if type(ins[1]) is str:
				stage.append(ins)
			else:
				stage.append(b'\xa5' + ins[1].to_bytes(2, signed=True))
			i = i + 3
			continue

		if isinstance(ins, list) and ins[0].__eq__('if_acmpne'):
			if type(ins[1]) is str:
				stage.append(ins)
			else:
				stage.append(b'\xa6' + ins[1].to_bytes(2, signed=True))
			i = i + 3
			continue

		if isinstance(ins, list) and ins[0].__eq__('goto'):
			if type(ins[1]) is str:
				stage.append(ins)
			else:
				stage.append(b'\xa7' + ins[1].to_bytes(2, signed=True))
			i = i + 3
			continue

		if isinstance(ins, list) and ins[0].__eq__('ifnull'):
			if type(ins[1]) is str:
				stage.append(ins)
			else:
				stage.append(b'\xc6' + ins[1].to_bytes(2, signed=True))
			i = i + 3
			continue

		if isinstance(ins, list) and ins[0].__eq__('ifnonnull'):
			if type(ins[1]) is str:
				stage.append(ins)
			else:
				stage.append(b'\xc7' + ins[1].to_bytes(2, signed=True))
			i = i + 3
			continue

		if isinstance(ins, list) and ins[0].__eq__('jsr'):
			if type(ins[1]) is str:
				stage.append(ins)
			else:
				stage.append(b'\xa8' + ins[1].to_bytes(2, signed=True))
			i = i + 3
			continue

		if isinstance(ins, list) and ins[0].__eq__('goto_w'):
			if type(ins[1]) is str:
				stage.append(ins)
			else:
				stage.append(b'\xc8' + ins[1].to_bytes(4, signed=True))
			i = i + 5
			continue

		if isinstance(ins, list) and ins[0].__eq__('jsr_w'):
			if type(ins[1]) is str:
				stage.append(ins)
			else:
				stage.append(b'\xc9' + ins[1].to_bytes(4, signed=True))
			i = i + 5
			continue

		if isinstance(ins, list) and eq(ins[0], 'ldc.i32'):
			stage.append(b'\x12' + icpx_int(cf, cp_cache, ins[1]).to_bytes(1))
			i = i + 2
			continue

		if isinstance(ins, list) and eq(ins[0], 'ldc.f32'):
			if isinstance(ins[1], bytes):
				stage.append(b'\x12' + icpx_float(cf, cp_cache, ins[1]).to_bytes(1))
			else:
				stage.append(b'\x12' + icpx_float(cf, cp_cache, struct.pack('>f', ins[1])).to_bytes(1))
			i = i + 2
			continue

		if isinstance(ins, list) and eq(ins[0], 'ldc.string'):
			stage.append(b'\x12' + icpx_string(cf, cp_cache, ins[1]).to_bytes(1))
			i = i + 2
			continue

		if isinstance(ins, list) and eq(ins[0], 'ldc.class'):
			stage.append(b'\x12' + icpx_c(cf, cp_cache, ins[1]).to_bytes(1))
			i = i + 2
			continue

		if isinstance(ins, list) and eq(ins[0], 'ldc.method_handle'):
			print('Err: not implemented.', file=stderr)
			exit(1)

		if isinstance(ins, list) and eq(ins[0], 'ldc.method_type'):
			print('Err: not implemented.', file=stderr)
			exit(1)

		if isinstance(ins, list) and eq(ins[0], 'ldc_w.i32'):
			stage.append(b'\x13' + i2cpx_int(cf, cp_cache, ins[1]))
			i = i + 3
			continue

		if isinstance(ins, list) and eq(ins[0], 'ldc_w.f32'):
			if isinstance(ins[1], bytes):
				stage.append(b'\x13' + i2cpx_float(cf, cp_cache, ins[1]))
			else:
				stage.append(b'\x13' + i2cpx_float(cf, cp_cache, struct.pack('>f', ins[1])))
			i = i + 3
			continue

		if isinstance(ins, list) and eq(ins[0], 'ldc_w.string'):
			stage.append(b'\x13' + i2cpx_string(cf, cp_cache, ins[1]))
			i = i + 3
			continue

		if isinstance(ins, list) and eq(ins[0], 'ldc_w.class'):
			stage.append(b'\x13' + i2cpx_c(cf, cp_cache, ins[1]))
			i = i + 3
			continue

		if isinstance(ins, list) and eq(ins[0], 'ldc_w.method_type'):
			print('Err: not implemented.', file=stderr)
			exit(1)

		if isinstance(ins, list) and eq(ins[0], 'ldc_w.method_handle'):
			print('Err: not implemented.', file=stderr)
			exit(1)

		if isinstance(ins, list) and eq(ins[0], 'ldc2_w.i64'):
			stage.append(b'\x14' + i2cpx_long(cf, cp_cache, ins[1]))
			i = i + 3
			continue

		if isinstance(ins, list) and eq(ins[0], 'ldc2_w.f64'):
			if isinstance(ins[1], bytes):
				stage.append(b'\x14' + i2cpx_double(cf, cp_cache, ins[1]))
			else:
				stage.append(b'\x14' + i2cpx_double(cf, cp_cache, struct.pack('>d', ins[1])))
			i = i + 3
			continue

		if isinstance(ins, list) and eq(ins[0], 'getstatic'):
			args = []

			for arg in ins[1:]:
				if isinstance(arg, tuple):
					args.append(arg[select])
				else:
					args.append(arg)

			stage.append(b'\xb2' + i2cpx_f(cf, cp_cache, *args))
			i = i + 3
			continue

		if isinstance(ins, list) and eq(ins[0], 'putstatic'):
			args = []

			for arg in ins[1:]:
				if isinstance(arg, tuple):
					args.append(arg[select])
				else:
					args.append(arg)

			stage.append(b'\xb3' + i2cpx_f(cf, cp_cache, *args))
			i = i + 3
			continue

		if isinstance(ins, list) and eq(ins[0], 'getfield'):
			args = []

			for arg in ins[1:]:
				if isinstance(arg, tuple):
					args.append(arg[select])
				else:
					args.append(arg)

			stage.append(
				b'\xb4' + i2cpx_f(cf, cp_cache, *args)
			)
			i = i + 3
			continue

		if isinstance(ins, list) and eq(ins[0], 'putfield'):
			args = []

			for arg in ins[1:]:
				if isinstance(arg, tuple):
					args.append(arg[select])
				else:
					args.append(arg)

			stage.append(b'\xb5' + i2cpx_f(cf, cp_cache, *args))
			i = i + 3
			continue

		if isinstance(ins, list) and eq(ins[0], 'new'):
			stage.append(b'\xbb' + i2cpx_c(cf, cp_cache, ins[1][select] if isinstance(ins[1], tuple) else ins[1]))
			i = i + 3
			continue

		if isinstance(ins, list) and eq(ins[0], 'newarray'):
			stage.append(b'\xbc' + ins[1].to_bytes(1))
			i = i + 2
			continue

		if isinstance(ins, list) and eq(ins[0], 'anewarray'):
			stage.append(b'\xbd' + i2cpx_c(cf, cp_cache, ins[1][select] if isinstance(ins[1], tuple) else ins[1]))
			i = i + 3
			continue

		if isinstance(ins, list) and eq(ins[0], 'checkcast'):
			stage.append(b'\xc0' + i2cpx_c(cf, cp_cache, ins[1][select] if isinstance(ins[1], tuple) else ins[1]))
			i = i + 3
			continue

		if isinstance(ins, list) and eq(ins[0], 'instanceof'):
			stage.append(b'\xc1' + i2cpx_c(cf, cp_cache, ins[1][select] if isinstance(ins[1], tuple) else ins[1]))
			i = i + 3
			continue

		if isinstance(ins, list) and eq(ins[0], 'invokevirtual'):
			args = []

			for arg in ins[1:]:
				if isinstance(arg, tuple):
					args.append(arg[select])
				else:
					args.append(arg)

			stage.append(
				b'\xb6' + i2cpx_m(cf, cp_cache, *args)
			)
			i = i + 3
			continue

		if isinstance(ins, list) and eq(ins[0], 'invokespecial'):
			args = []

			for arg in ins[1:]:
				if isinstance(arg, tuple):
					args.append(arg[select])
				else:
					args.append(arg)

			stage.append(
				b'\xb7' + i2cpx_m(cf, cp_cache, *args)
			)
			i = i + 3
			continue

		if isinstance(ins, list) and eq(ins[0], 'invokestatic'):
			args = []

			for arg in ins[1:]:
				if isinstance(arg, tuple):
					args.append(arg[select])
				else:
					args.append(arg)

			stage.append(
				b'\xb8' + i2cpx_m(cf, cp_cache, *args)
			)
			i = i + 3
			continue

		if isinstance(ins, list) and eq(ins[0], 'invokeinterface'):
			args = []

			for arg in ins[1:4]:
				if isinstance(arg, tuple):
					args.append(arg[select])
				else:
					args.append(arg)

			stage.append(b'\xb9' + i2cpx_i(cf, cp_cache, *args) + ins[4].to_bytes(1) + b'\x00')
			i = i + 5
			continue

		if isinstance(ins, list) and eq(ins[0], 'label'):
			target_table[ins[1]] = i
			continue

		if ins[0] in ('invokedynamic', 'multianewarray', 'wide', 'tableswitch', 'lookupswitch'):
			print('Err: unimplemented.', file=stderr)
			exit(1)

		print('Err: unknown instruction.', file=stderr)
		exit(1)

	i = pc_begin

	for j, ins in enumerate(stage):
		if isinstance(ins, bytes):
			i = i + len(ins)
		else:
			name_to_opcode = {
				'ifeq': b'\x99',
				'ifne': b'\x9a',
				'iflt': b'\x9b',
				'ifge': b'\x9c',
				'ifgt': b'\x9d',
				'ifle': b'\x9e',
				'if_icmpeq': b'\x9f',
				'if_icmpne': b'\xa0',
				'if_icmplt': b'\xa1',
				'if_icmpge': b'\xa2',
				'if_icmpgt': b'\xa3',
				'if_icmple': b'\xa4',
				'if_acmpeq': b'\xa5',
				'if_acmpne': b'\xa6',
				'goto': b'\xa7',
				'ifnull': b'\xc6',
				'ifnonnull': b'\xc7',
				'jsr': b'\xa8',
				'goto_w': b'\xc8',
				'jsr_w': b'\xc9',
			}

			target_pc = target_table[ins[1]]
			offset_pc = target_pc - i

			stage[j] = name_to_opcode[ins[0]] + offset_pc.to_bytes(2, signed=True)
			i = i + 3

	return b''.join(stage)
