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
from modmaker.utf8 import utf8_encode

def apply():
	if not mod.config.is_one_of_features_enabled(['etc.log_version', 'blackbox']):
		return

	cf = load_class_file(mod.config.path('stage/server/net/minecraft/server/MinecraftServer.class'))

	if mod.config.is_feature_enabled('etc.log_version'):
		for entry in cf[0x04]:
			if entry[0].__eq__(452):
				entry[2] = len(f'Crab Pack {mod.version}').to_bytes(2)
				entry[3] = utf8_encode(f'Crab Pack {mod.version}')

	cp_cache = cp_init_cache(cf[0x04])

	if mod.config.is_feature_enabled('blackbox'):
		_modify_init_method(cf, cp_cache)
		_modify_shutdown_method(cf, cp_cache)

	with open(mod.config.path('stage/server/net/minecraft/server/MinecraftServer.class'), 'wb') as file:
		file.write(cf_assemble(cf))

	print('Patched net.minecraft.server.MinecraftServer')

def _modify_init_method(cf, cp_cache):
	m = get_method(cf, cp_cache, 'c', '()Z')
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = a_code_load(a[0x02])

	a_code[0x03] = a_code[0x03][0:-2] + assemble_code(cf, cp_cache, 1, len(a_code[0x03][0:-2]), [
		['getstatic', 'com/thebluetropics/crabpack/Blackbox', 'INSTANCE', 'Lcom/thebluetropics/crabpack/Blackbox;'],
		['invokevirtual', 'com/thebluetropics/crabpack/Blackbox', 'startServer', '()V'],
		'iconst_1',
		'ireturn'
	])

	a_code[0x02] = len(a_code[0x03]).to_bytes(4)
	a_code[0x06] = (int.from_bytes(a_code[0x06]) - 1).to_bytes(2)

	for i, a in a_code[0x07]:
		if get_utf8_at(cp_cache, int.from_bytes(a[0x00])).__eq__('LineNumberTable'):
			del a_code[0x07][i]
			break

	a[0x02] = a_code_assemble(a_code)
	a[0x01] = len(a[0x02]).to_bytes(4)

def _modify_shutdown_method(cf, cp_cache):
	m = get_method(cf, cp_cache, 'g', '()V')
	a = get_attribute(m[0x04], cp_cache, 'Code')

	a_code = a_code_load(a[0x02])

	a_code[0x03] = assemble_code(cf, cp_cache, 1, 0, [
		['getstatic', 'com/thebluetropics/crabpack/Blackbox', 'INSTANCE', 'Lcom/thebluetropics/crabpack/Blackbox;'],
		['invokevirtual', 'com/thebluetropics/crabpack/Blackbox', 'stopServer', '()V']
	]) + a_code[0x03]

	a_code[0x02] = len(a_code[0x03]).to_bytes(4)
	a_code[0x06] = (int.from_bytes(a_code[0x06]) - 1).to_bytes(2)

	for i, a in a_code[0x07]:
		if get_utf8_at(cp_cache, int.from_bytes(a[0x00])).__eq__('LineNumberTable'):
			del a_code[0x07][i]
			break

	a[0x02] = a_code_assemble(a_code)
	a[0x01] = len(a[0x02]).to_bytes(4)
