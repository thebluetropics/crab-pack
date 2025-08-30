import mod

from mod.jvm import (
	class_file,
	attribute,
	constant_pool,
	get_method,
	get_attribute,
	get_utf8_at
)

def apply_client():
	if not mod.config.is_feature_enabled('stackable_food'):
		return

	cf = class_file.load(mod.config.path('stage/client/yw.class'))
	xcp = constant_pool.use_helper(cf)

	m = get_method(cf, xcp, '<init>', '(IIZ)V')
	a = get_attribute(m[0x04], xcp, 'Code')

	a_code = attribute.code.load(a[0x02])

	code = bytearray(a_code[0x03])
	del code[16]
	code[16:16] = b'\x10' + b'\x10' # bipush 16
	a_code[0x03] = bytes(code)

	# update code length
	a_code[0x02] = len(a_code[0x03]).to_bytes(4)

	# remove line number table
	a_code[0x06] = (int.from_bytes(a_code[0x06]) - 1).to_bytes(2)

	for i, a in a_code[0x07]:
		if get_utf8_at(xcp, int.from_bytes(a[0x00])).__eq__('LineNumberTable'):
			del a_code[0x07][i]
			break

	# update code attribute
	a[0x02] = attribute.code.assemble(a_code)

	# update code attribute length
	a[0x01] = len(a[0x02]).to_bytes(4)

	with open(mod.config.path('stage/client/yw.class'), 'wb') as file:
		file.write(class_file.assemble(cf))

	print('Patched client:yw.class → net.minecraft.item.FoodItem')

def apply_server():
	if not mod.config.is_feature_enabled('stackable_food'):
		return

	cf = class_file.load(mod.config.path('stage/server/px.class'))
	xcp = constant_pool.use_helper(cf)

	m = get_method(cf, xcp, '<init>', '(IIZ)V')
	a = get_attribute(m[0x04], xcp, 'Code')

	a_code = attribute.code.load(a[0x02])

	code = bytearray(a_code[0x03])
	del code[16]
	code[16:16] = b'\x10' + b'\x10' # bipush 16
	a_code[0x03] = bytes(code)

	# update code length
	a_code[0x02] = len(a_code[0x03]).to_bytes(4)

	# remove line number table
	a_code[0x06] = (int.from_bytes(a_code[0x06]) - 1).to_bytes(2)

	for i, a in a_code[0x07]:
		if get_utf8_at(xcp, int.from_bytes(a[0x00])).__eq__('LineNumberTable'):
			del a_code[0x07][i]
			break

	# update code attribute
	a[0x02] = attribute.code.assemble(a_code)

	# update code attribute length
	a[0x01] = len(a[0x02]).to_bytes(4)

	with open(mod.config.path('stage/server/px.class'), 'wb') as file:
		file.write(class_file.assemble(cf))

	print('Patched server:px.class → net.minecraft.item.FoodItem')
