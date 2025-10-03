import mod

from modmaker.a import (
	get_attribute
)
from modmaker.a_code import (
	a_code_load,
	a_code_assemble
)
from modmaker.m import(
	get_method
)
from modmaker.cf import (
	load_class_file,
	cf_assemble
)
from modmaker.cp import (
	cp_init_cache,
	get_utf8_at
)

def apply():
	if not mod.config.is_feature_enabled('user_interface.minimal_title_screen'):
		return

	cf = load_class_file(mod.config.path('stage/client/fu.class'))
	cp_cache = cp_init_cache(cf[0x04])

	m = get_method(cf, cp_cache, 'a', '(IIF)V')
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = a_code_load(a[0x02])

	a_code[0x03] = a_code[0x03][0:104] + a_code[0x03][227:len(a_code[0x03])]
	a_code[0x02] = len(a_code[0x03]).to_bytes(4)
	a_code[0x06] = (int.from_bytes(a_code[0x06]) - 1).to_bytes(2)

	for i, a in a_code[0x07]:
		if get_utf8_at(cp_cache, int.from_bytes(a[0x00])).__eq__('LineNumberTable'):
			del a_code[0x07][i]
			break

	a[0x02] = a_code_assemble(a_code)
	a[0x01] = len(a[0x02]).to_bytes(4)

	with open(mod.config.path('stage/client/fu.class'), 'wb') as f:
		f.write(cf_assemble(cf))

	print('Patched client:fu.class → net.minecraft.client.gui.screen.TitleScreen')
