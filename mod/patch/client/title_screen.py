import mod

from mod.attribute import get_attribute
from mod.method import get_method
from mod.constant_pool import get_utf8_at
from mod import (
	class_file,
	attribute,
	constant_pool
)


def apply():
	if not mod.config.is_feature_enabled('user_interface.minimal_title_screen'):
		return

	cf = class_file.load(mod.config.path('stage/client/fu.class'))
	cp_cache = constant_pool.init_constant_pool_cache(cf[0x04])

	m = get_method(cf, cp_cache, 'a', '(IIF)V')
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = attribute.code.load(a[0x02])

	# modify code
	code = bytearray(a_code[0x03])
	del code[104:227]
	a_code[0x03] = bytes(code)

	# update code length
	a_code[0x02] = len(a_code[0x03]).to_bytes(4)

	# remove line number table
	a_code[0x06] = (int.from_bytes(a_code[0x06]) - 1).to_bytes(2)

	for i, a in a_code[0x07]:
		if get_utf8_at(cp_cache, int.from_bytes(a[0x00])).__eq__('LineNumberTable'):
			del a_code[0x07][i]
			break

	# update code attribute
	a[0x02] = attribute.code.assemble(a_code)

	# update code attribute length
	a[0x01] = len(a[0x02]).to_bytes(4)

	with open(mod.config.path('stage/client/fu.class'), 'wb') as f:
		f.write(class_file.assemble(cf))

	print('Patched client:fu.class → net.minecraft.client.gui.screen.TitleScreen')
