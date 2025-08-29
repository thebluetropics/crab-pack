import mod

from mod.bytecode.method import get_method
from mod.bytecode.attribute import get_attribute
from mod.bytecode import (
	class_file,
	code_attribute,
	instructions,
	constant_pool
)

def apply(side_name):
	if not mod.config.is_feature_enabled('no_crop_trampling'):
		return

	side = 0 if side_name.__eq__('client') else 1

	c_name = ['vl', 'no'][side]
	cf = class_file.load(mod.config.path(f'stage/{side_name}/{c_name}.class'))

	m = get_method(cf, cf[0x04], 'b', ['(Lfd;IIILsn;)V', '(Ldj;IIILlq;)V'][side])
	a = get_attribute(m[0x04], cf[0x04], 'Code')

	a_code = code_attribute.load(a[0x02])

	a_code[0x03] = instructions.make(0, [
		'return'
	])

	# update code length
	a_code[0x02] = len(a_code[0x03]).to_bytes(4)

	# remove line number table
	a_code[0x06] = (int.from_bytes(a_code[0x06]) - 1).to_bytes(2)

	for i, a in a_code[0x07]:
		if constant_pool.get_utf8(cf[0x04], int.from_bytes(a[0x00])).__eq__('LineNumberTable'):
			del a_code[0x07][i]
			break

	# update code attribute
	a[0x02] = code_attribute.assemble(a_code)

	# update code attribute length
	a[0x01] = len(a[0x02]).to_bytes(4)

	with open(mod.config.path(f'stage/{side_name}/{c_name}.class'), 'wb') as file:
		file.write(class_file.make(cf))

	print(f'Patched {side_name}:{c_name}.class → net.minecraft.block.FarmlandBlock')
