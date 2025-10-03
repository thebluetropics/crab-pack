import mod

from modmaker.a import (
	get_attribute
)
from modmaker.a_code import (
	a_code_load,
	a_code_assemble,
	assemble_code
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
	if not mod.config.is_feature_enabled('blackbox'):
		return

	cf = load_class_file(mod.config.path('stage/server/fc.class'))
	cp_cache = cp_init_cache(cf[0x04])

	_modify_disconnect_method(cf, cp_cache)

	with open(mod.config.path('stage/server/fc.class'), 'wb') as file:
		file.write(cf_assemble(cf))

	print('Patched server:fc.class → net.minecraft.server.PlayerManager')

def _modify_disconnect_method(cf, cp_cache):
	m = get_method(cf, cp_cache, 'e', '(Ldl;)V')
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = a_code_load(a[0x02])

	a_code[0x03] = assemble_code(cf, cp_cache, 1, 0, [
		['getstatic', 'com/thebluetropics/crabpack/Blackbox', 'INSTANCE', 'Lcom/thebluetropics/crabpack/Blackbox;'],
		'aload_1', ['getfield', 'dl', 'r', 'Ljava/lang/String;'],
		['invokevirtual', 'com/thebluetropics/crabpack/Blackbox', 'onPlayerLeft', '(Ljava/lang/String;)V'],
	]) + a_code[0x03]

	a_code[0x02] = len(a_code[0x03]).to_bytes(4)
	a_code[0x06] = (int.from_bytes(a_code[0x06]) - 1).to_bytes(2)

	for i, a in a_code[0x07]:
		if get_utf8_at(cp_cache, int.from_bytes(a[0x00])).__eq__('LineNumberTable'):
			del a_code[0x07][i]
			break

	a[0x02] = a_code_assemble(a_code)
	a[0x01] = len(a[0x02]).to_bytes(4)
